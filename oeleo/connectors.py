import getpass
import hashlib
import logging
import os
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Protocol, Iterator, List

from fabric import Connection

from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from shareplum.errors import ShareplumRequestError

from oeleo.filters import base_filter
from oeleo.movers import simple_mover
from oeleo.utils import calculate_checksum

log = logging.getLogger("oeleo")

FabricRunResult = Any
Hash = str


def register_password(pwd: str = None) -> None:
    """Helper function to export the password as an environmental variable"""
    log.debug(" -> Register password ")
    if pwd is None:
        # Consider replacing this with the Rich prompt.
        session_password = getpass.getpass(prompt="Password: ")
        os.environ["OELEO_PASSWORD"] = session_password
    log.debug(" Password registered!")


class Connector(Protocol):
    """Connectors are used to establish a connection to the directory and
    provide the functions and methods needed for the movers and checkers.
    """

    directory = None

    def connect(self, **kwargs) -> None:
        ...

    def close(self) -> None:
        ...

    def base_filter_sub_method(
        self, glob_pattern: str = "*", **kwargs
    ) -> Iterator[Path]:
        ...

    def calculate_checksum(self, f: Path, hide: bool = True) -> Hash:
        ...

    def move_func(self, path: Path, to: Path, *args, **kwargs) -> bool:
        ...


class LocalConnector(Connector):
    def __init__(self, directory=None):
        # TODO: check if it is best to default to TO DIR or FROM DIR or if it should break instead
        if directory is not None:
            self.directory = directory
        else:
            self.directory = os.environ["OELEO_BASE_DIR_FROM"]
            log.debug(
                "No directory passed to LocalConnector, defaulting to OELEO_BASE_DIR_FROM:",
                self.directory,
            )

        self.directory = Path(self.directory)

    def __str__(self):
        text = "LocalConnector"
        text += f"{self.directory=}\n"
        return text

    def connect(self, **kwargs) -> None:
        pass

    def close(self):
        pass

    def base_filter_sub_method(
        self, glob_pattern: str = "*", **kwargs
    ) -> Iterator[Path]:  # RENAME TO enquire
        return base_filter(self.directory, extension=glob_pattern)

    def calculate_checksum(self, f: Path, hide: bool = True) -> Hash:
        return calculate_checksum(f)

    def move_func(self, path: Path, to: Path, *args, **kwargs) -> bool:
        return simple_mover(path, to, *args, **kwargs)


class SSHConnector(Connector):
    def __init__(
        self,
        username=None,
        host=None,
        directory=None,
        is_posix=True,
        use_password=False,
    ):
        self.session_password = os.environ["OELEO_PASSWORD"]
        self.username = username or os.environ["OELEO_USERNAME"]
        self.host = host or os.environ["OELEO_EXTERNAL_HOST"]

        if directory is not None:
            self.directory = directory
        else:
            self.directory = os.environ["OELEO_BASE_DIR_TO"]
            log.debug(
                "No directory passed to SSHConnector, defaulting to OELEO_BASE_DIR_TO:",
                self.directory,
            )

        self.is_posix = is_posix
        self.use_password = use_password
        self.c = None
        self._validate()

    def __str__(self):
        text = "SSHConnector"
        text += f"{self.username=}\n"
        text += f"{self.host=}\n"
        text += f"{self.directory=}\n"
        text += f"{self.is_posix=}\n"
        text += f"{self.c=}\n"

        return text

    def _validate(self):
        if self.is_posix:
            self.directory = PurePosixPath(self.directory)
            log.debug("On posix")
            if str(self.directory).startswith(r"\\"):
                log.warning("YOUR PATH STARTS WITH WINDOWS TYPE SEPARATOR")
        else:
            self.directory = PureWindowsPath(self.directory)
            log.debug("Not on posix")
        log.debug(f"The ssh directory is: {self.directory}")

    def connect(self, **kwargs) -> None:
        if self.use_password:
            connect_kwargs = {
                "password": os.environ["OELEO_PASSWORD"],
            }
        else:
            connect_kwargs = {
                "key_filename": [os.environ["OELEO_KEY_FILENAME"]],
            }
        self.c = Connection(
            host=self.host, user=self.username, connect_kwargs=connect_kwargs
        )

    def __check_connection_and_exit(self):
        log.debug("Connected?")
        cmd = f"find {self.directory} -maxdepth 1 -name '*'"
        log.debug(cmd)
        self.c.run(cmd)
        sys.exit()

    def close(self):
        self.c.close()

    def __delete__(self, instance):
        if self.c is not None:
            self.c.close()

    def base_filter_sub_method(self, glob_pattern: str = "", **kwargs: Any) -> list:
        log.debug("base filter function for SSHConnector")
        log.debug("got this glob pattern:")
        log.debug(f"{glob_pattern}")

        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        result = self._list_content(f"*{glob_pattern}", hide=True)
        file_list = result.stdout.strip().split("\n")
        if self.is_posix:
            file_list = [PurePosixPath(f) for f in file_list]
        else:
            file_list = [Path(f) for f in file_list]  # OBS Linux -> Win not supported!

        return file_list

    def _list_content(self, glob_pattern="*", max_depth=1, hide=False):

        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        cmd = f"find {self.directory} -maxdepth {max_depth} -name '{glob_pattern}'"
        log.debug(cmd)
        result = self.c.run(cmd, hide=hide)
        if not result.ok:
            log.debug("it failed - should raise an exception her (future work)")
        return result

    def calculate_checksum(self, f, hide=True):
        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        cmd = f"md5sum {self.directory/f}"
        result = self.c.run(cmd, hide=hide)
        if not result.ok:
            log.debug("it failed - should raise an exception her (future work)")
        checksum = result.stdout.strip().split()[0]
        return checksum

    def move_func(self, path: Path, to: Path, *args, **kwargs) -> bool:
        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        try:
            log.debug(f"Copying {path} to {to}")
            self.c.put(str(path), remote=str(to))
        except Exception as e:
            log.debug("GOT AN EXCEPTION DURING COPYING FILE")
            log.debug(f"FROM     : {path}")
            log.debug(f"TO       : {to}")
            log.debug(f"EXCEPTION:")
            log.debug(e)
            return False
        return True


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

    @staticmethod
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

    def __delete__(self, instance):
        if self.connection is not None:
            self.connection.close()

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

        except ShareplumRequestError:
            return False

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
            log.debug(f"EXCEPTION:")
            log.debug(e)
            return False

        except Exception as e:
            log.debug("GOT AN EXCEPTION DURING COPYING FILE")
            log.debug(f"FROM     : {path}")
            log.debug(f"TO       : {to}")
            log.debug(f"EXCEPTION:")
            log.debug(e)
            return False

        return True
