import getpass
import hashlib
import logging
import os
import shlex
import sys
import time
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Protocol, Iterator, List, Union

from fabric import Connection

from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from shareplum.errors import ShareplumRequestError

from oeleo.filters import base_filter, additional_filtering
from oeleo.movers import simple_mover, simple_recursive_mover
from oeleo.utils import calculate_checksum

CONNECTION_RETRIES = 3


log = logging.getLogger("oeleo")

FabricRunResult = Any
Hash = str


class OeleoConnectionError(Exception):
    """Raised when a connection cannot be established or remote listing fails."""

    pass


class OeleoTransferError(Exception):
    """Raised when a connected file operation (e.g. checksum) fails."""

    pass


def register_password(pwd: str = None) -> None:
    """Helper function to export the password as an environmental variable"""
    log.debug(" -> Register password ")
    if pwd is None:
        # Consider replacing this with the Rich prompt.
        session_password = getpass.getpass(prompt="Password: ")
    else:
        session_password = pwd
    os.environ["OELEO_PASSWORD"] = session_password
    log.debug(" Password registered!")


class Connector(Protocol):
    """Connectors are used to establish a connection to the directory and
    provide the functions and methods needed for the movers and checkers.
    """

    directory = None
    is_local = True
    include_subdirs = False

    def connect(self, **kwargs) -> None:
        ...

    def reconnect(self, **kwargs) -> None:
        self.close()
        self.connect()

    def close(self) -> None:
        ...

    def base_filter_sub_method(
        self, glob_pattern: str = "*", **kwargs
    ) -> Union[Iterator[Path], List[Path]]:
        ...

    def calculate_checksum(self, f: Path, hide: bool = True) -> Hash:
        ...

    def move_func(self, path: Path, to: Path, *args, **kwargs) -> bool:
        ...

    def ensure_connection(self) -> None:
        """Raise OeleoConnectionError if the destination is unreachable."""
        ...


class LocalConnector(Connector):
    def __init__(self, directory=None, **kwargs):
        # TODO: check if it is best to default to TO DIR or FROM DIR or if it should break instead
        if directory is not None:
            self.directory = directory
        else:
            self.directory = os.environ["OELEO_BASE_DIR_FROM"]
            log.debug(
                f"No directory passed to LocalConnector, defaulting to OELEO_BASE_DIR_FROM: {self.directory}"
            )

        self.directory = Path(self.directory)
        self.include_subdirs = kwargs.pop("include_subdirs", False)

    def __str__(self):
        return f"LocalConnector\n{self.directory=}\n"

    def connect(self, **kwargs) -> None:
        pass

    def reconnect(self, **kwargs) -> None:
        pass

    def close(self):
        pass

    def ensure_connection(self) -> None:
        path = Path(self.directory)
        try:
            if not path.exists() or not path.is_dir():
                raise OeleoConnectionError(
                    f"Local destination not available: {path}"
                )
            path.stat()
            if not os.access(path, os.R_OK | os.X_OK):
                raise OeleoConnectionError(
                    f"Local destination not accessible: {path}"
                )
        except OeleoConnectionError:
            raise
        except OSError as e:
            raise OeleoConnectionError(
                f"Local destination not available: {path}"
            ) from e

    def base_filter_sub_method(
        self, glob_pattern: str = "*", **kwargs
    ) -> Iterator[Path]:  # RENAME TO enquire
        log.debug("base filter function for LocalConnector")
        log.debug(f"{self.directory}")
        log.debug(f"{self.include_subdirs=}")
        if self.include_subdirs:
            base_filter_func = self.directory.rglob
        else:
            base_filter_func = self.directory.glob

        file_list = base_filter(
            self.directory, extension=glob_pattern, base_filter_func=base_filter_func
        )
        logging.debug(f"Got {file_list} files")

        if additional_filters := kwargs.get("additional_filters"):
            file_list = additional_filtering(file_list, additional_filters)
        return file_list

    def calculate_checksum(self, f: Path, hide: bool = True) -> Hash:
        return calculate_checksum(f)

    def move_func(self, path: Path, to: Path, *args, **kwargs) -> bool:
        log.debug("\nmove_func function for LocalConnector")
        log.debug(f"{path=}")
        log.debug(f"{to=}")
        log.debug(f"{self.directory}")
        log.debug(f"{self.include_subdirs=}")
        if self.include_subdirs:
            return simple_recursive_mover(path, to, *args, **kwargs)
        return simple_mover(path, to, *args, **kwargs)


class SSHConnector(Connector):
    is_local = False

    def __init__(
        self,
        username=None,
        host=None,
        directory=None,
        is_posix=True,
        use_password=False,
        include_subdirs=False,
    ):
        self.use_password = use_password
        if self.use_password:
            try:
                self.session_password = os.environ["OELEO_PASSWORD"]
            except KeyError as e:
                raise ValueError(
                    "OELEO_PASSWORD is required when use_password=True"
                ) from e
        else:
            self.session_password = None

        self.username = username or os.environ["OELEO_USERNAME"]
        self.host = host or os.environ["OELEO_EXTERNAL_HOST"]

        if directory is not None:
            self.directory = directory
        else:
            self.directory = os.environ["OELEO_BASE_DIR_TO"]
            log.debug(
                f"No directory passed to SSHConnector, defaulting to OELEO_BASE_DIR_TO: {self.directory}"
            )

        self.is_posix = is_posix
        self.include_subdirs = include_subdirs
        self.c = None
        self._validate()

    def __str__(self):
        text = "SSHConnector"
        text += f"{self.username=}\n"
        text += f"{self.host=}\n"
        text += f"{self.directory=}\n"
        text += f"{self.is_posix=}\n"
        text += f"{self.use_password=}\n"
        text += f"{self.include_subdirs=}\n"
        text += f"{self.c=}\n"

        return text

    def _validate(self):
        if self.is_posix:
            self.directory = PurePosixPath(self.directory)
            log.debug("SSHConnector:ON POSIX")
            if str(self.directory).startswith(r"\\"):
                log.warning("YOUR PATH STARTS WITH WINDOWS TYPE SEPARATOR")
        else:
            self.directory = PureWindowsPath(self.directory)
            log.debug("Not on posix")
        log.debug(f"The ssh directory is: {self.directory}")

    def _remote_shell_token(self, value: Any) -> str:
        """Quote a path/token for remote shell interpolation (SEC-01).

        POSIX remotes use ``shlex.quote`` (the supported / tested path).
        Windows remotes get a best-effort ``cmd.exe`` double-quote wrap only;
        full Windows shell safety is not claimed without a dedicated harness.
        """
        text = str(value)
        if self.is_posix:
            return shlex.quote(text)
        return '"' + text.replace('"', '""') + '"'

    def connect(self, **kwargs) -> None:
        if self.use_password:
            password = self.session_password
            if password is None:
                try:
                    password = os.environ["OELEO_PASSWORD"]
                except KeyError as e:
                    raise ValueError(
                        "OELEO_PASSWORD is required when use_password=True"
                    ) from e
            connect_kwargs = {"password": password}
        else:
            connect_kwargs = {
                "key_filename": [os.environ["OELEO_KEY_FILENAME"]],
            }
        self.c = Connection(
            host=self.host, user=self.username, connect_kwargs=connect_kwargs
        )

    def reconnect(self, **kwargs) -> None:
        try:
            self.close()
        except Exception as e:
            log.debug(f"Got an exception during closing connection: {e}")
            raise OeleoConnectionError("Could not close connection")
        try:
            self.connect()
        except Exception as e:
            log.debug(f"Got an exception during connecting: {e}")
            raise OeleoConnectionError("Could not connect")

    def ensure_connection(self) -> None:
        if self.c is None:
            try:
                self.connect()
            except Exception as e:
                raise OeleoConnectionError("Could not connect") from e
        try:
            remote_q = self._remote_shell_token(self.directory)
            if self.is_posix:
                cmd = f"test -d {remote_q}"
            else:
                cmd = f"if not exist {remote_q} exit /b 1"
            result = self.c.run(cmd, hide=True, in_stream=False, warn=True)
            if not result.ok:
                raise OeleoConnectionError(
                    f"Remote destination not available: {self.directory}"
                )
        except OeleoConnectionError:
            raise
        except Exception as e:
            raise OeleoConnectionError(
                f"Lost connection to remote destination: {self.directory}"
            ) from e

    def _check_connection_and_exit(self):
        # used only when developing oeleo
        log.debug("Connected?")
        if self.is_posix:
            cmd = (
                f"find {self._remote_shell_token(self.directory)} "
                f"-maxdepth 1 -name {self._remote_shell_token('*')}"
            )
            log.debug(cmd)
            self.c.run(cmd)
        else:
            cmd = f"dir {self._remote_shell_token(self.directory)}"
            log.debug(cmd)
            self.c.run(cmd)
        sys.exit()

    def check_connection_and_exit(self):
        log.debug("Connected?")
        if self.is_posix:
            cmd = (
                f"find {self._remote_shell_token(self.directory)} "
                f"-maxdepth 1 -name {self._remote_shell_token('*')}"
            )
            log.debug(cmd)
            self.c.run(cmd)
        else:
            cmd = f"dir {self._remote_shell_token(self.directory)}"
            log.debug(cmd)
            self.c.run(cmd)
        sys.exit()

    def close(self):
        self.c.close()

    def base_filter_sub_method(self, glob_pattern: str = "", **kwargs: Any) -> list:
        log.debug("base filter function for SSHConnector")
        log.debug("got this glob pattern:")
        log.debug(f"{glob_pattern}")

        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        max_depth = None if self.include_subdirs else 1
        file_list = self._list_content(
            f"*{glob_pattern}",
            hide=True,
            max_depth=max_depth,
        )

        # experimental feature:
        if additional_filters := kwargs.get("additional_filters"):
            logging.debug(
                f"Got additional_filters for SSHConnector. This is not implemented yet! {additional_filters}"
            )

            # file_list = additional_filtering(file_list, additional_filters)

        if self.is_posix:
            file_list = [PurePosixPath(f) for f in file_list]
        else:
            file_list = [
                Path(f) for f in file_list
            ]  # OBS Linux -> Win not supported yet!

        return file_list

    def _list_content(self, glob_pattern="*", max_depth=1, hide=False):
        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        directory_q = self._remote_shell_token(self.directory)
        pattern_q = self._remote_shell_token(glob_pattern)
        if max_depth is None:
            cmd = f"find {directory_q} -name {pattern_q}"
        else:
            depth = int(max_depth)
            cmd = f"find {directory_q} -maxdepth {depth} -name {pattern_q}"
        log.debug(cmd)
        try:
            result = self.c.run(cmd, hide=hide, in_stream=False)
        except OeleoConnectionError:
            raise
        except Exception as e:
            log.debug(f"Encountered an exception from fabric: {e}")
            raise OeleoConnectionError(
                f"Failed to list remote content: {self.directory}"
            ) from e

        if not result.ok:
            log.debug("Encountered an error from fabric during remote list")
            raise OeleoConnectionError(
                f"Failed to list remote content: {self.directory}"
            )

        stdout = (result.stdout or "").strip()
        if not stdout:
            return []
        return [line for line in stdout.split("\n") if line]

    def calculate_checksum(self, f, hide=True):
        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        cmd = f"md5sum {self._remote_shell_token(self.directory / f)}"
        try:
            result = self.c.run(cmd, hide=hide, in_stream=False)
        except OeleoTransferError:
            raise
        except Exception as e:
            log.debug(f"Encountered an exception from fabric during checksum: {e}")
            raise OeleoTransferError(
                f"Failed to calculate checksum for {f}"
            ) from e

        if not result.ok:
            raise OeleoTransferError(f"Failed to calculate checksum for {f}")

        parts = (result.stdout or "").strip().split()
        if not parts:
            raise OeleoTransferError(
                f"Failed to calculate checksum for {f}: empty output"
            )
        return parts[0]

    def _ensure_remote_dir(self, remote_dir: Path) -> None:
        if self.c is None:
            log.debug("Connecting ...")
            self.connect()

        remote_q = self._remote_shell_token(remote_dir)
        if self.is_posix:
            cmd = f"mkdir -p {remote_q}"
        else:
            # Best-effort cmd.exe quoting only; POSIX is the SEC-01 acceptance path.
            cmd = f"if not exist {remote_q} mkdir {remote_q}"

        log.debug(f"Ensuring remote dir exists: {remote_dir}")
        self.c.run(cmd, hide=True, in_stream=False)

    def move_func(self, path: Path, to: Path, *args, **kwargs) -> bool:
        exceptions = []
        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        for i in range(CONNECTION_RETRIES):
            try:
                self._ensure_remote_dir(to.parent)
                log.debug(f"Copying {path} to {to}")
                self.c.put(str(path), remote=str(to))
                return True
            except Exception as e:
                log.debug(f"Got an exception during moving file: {e}")
                log.debug(f"Retrying {i+1}/{CONNECTION_RETRIES}")
                exceptions.append(str(e))
                time.sleep(1)
                self.reconnect()

        log.debug("GOT A CRITICAL EXCEPTIONS DURING COPYING FILE")
        log.debug(f"FROM     : {path}")
        log.debug(f"TO       : {to}")
        log.debug(f"EXCEPTIONS: {exceptions}")
        return False


class SharePointConnection:
    def __init__(self, url, site_name, username, password, doc_library):
        self.site_url = "/".join([url, "sites", site_name])
        self.authcookie = Office365(
            url, username=username, password=password
        ).GetCookies()

        self.site = Site(
            self.site_url, version=Version.v365, authcookie=self.authcookie
        )
        self.folder = self.site.Folder(doc_library)

    def close(self):
        pass


class SharePointConnector(Connector):
    def __init__(
        self,
        username=None,
        host=None,
        url=None,
        directory=None,
    ):
        self.username = username or os.environ["OELEO_USERNAME"]
        self.session_password = os.environ["OELEO_PASSWORD"]
        self.url = url or os.environ["OELEO_SHAREPOINT_URL"]

        self.site_name = host or os.environ["OELEO_SHAREPOINT_SITENAME"]
        self.directory = directory or os.environ["OELEO_SHAREPOINT_DOC_LIBRARY"]
        self.connection = None

    def __str__(self):
        text = "SharePointConnector"
        text += f"{self.username=}\n"
        text += f"{self.url=}\n"
        text += f"{self.site_name=}\n"
        text += f"{self.directory=}\n"
        text += f"{self.connection=}\n"

        return text

    def connect(self, **kwargs) -> None:
        self.connection = SharePointConnection(
            url=self.url,
            site_name=self.site_name,
            username=self.username,
            password=self.session_password,
            doc_library=self.directory,
        )

    def close(self):
        self.connection.close()

    def ensure_connection(self) -> None:
        try:
            if self.connection is None:
                self.connect()
            # Touch the doc library listing; any transport/auth failure aborts.
            _ = self.connection.folder.files
        except OeleoConnectionError:
            raise
        except Exception as e:
            raise OeleoConnectionError(
                "SharePoint destination not available"
            ) from e

    def base_filter_sub_method(
        self, glob_pattern: str = "", **kwargs: Any
    ) -> List[Path]:
        file_list = []
        request = self.connection.folder.files
        for f in request:
            filename = f.get("Name", "")
            if filename and glob_pattern in filename:
                file_list.append(Path(filename))
        return file_list

    def calculate_checksum(self, f: Path, hide=True):
        try:
            b = self.connection.folder.get_file(f.name)
        except ShareplumRequestError as e:
            raise OeleoTransferError(
                f"Failed to calculate checksum for {f}"
            ) from e
        except Exception as e:
            raise OeleoTransferError(
                f"Failed to calculate checksum for {f}"
            ) from e

        file_hash = hashlib.md5(b)
        return file_hash.hexdigest()

    def move_func(self, path: Path, to: Path, *args, **kwargs) -> bool:
        try:
            log.debug(f"Copying {path} to {to}")
            file_content = path.read_bytes()
            self.connection.folder.upload_file(file_content, path.name)

        except ShareplumRequestError as e:
            log.debug("GOT A ShareplumRequestError EXCEPTION DURING COPYING FILE")
            log.debug(f"FROM     : {path}")
            log.debug(f"TO       : {to}")
            log.debug(f"EXCEPTION: {e}")
            return False

        except Exception as e:
            log.debug("GOT AN EXCEPTION DURING COPYING FILE")
            log.debug(f"FROM     : {path}")
            log.debug(f"TO       : {to}")
            log.debug(f"EXCEPTION: {e}")
            return False

        return True
