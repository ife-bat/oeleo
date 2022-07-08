import getpass
import logging
import os
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Generator, Protocol, Union

from fabric import Connection

from oeleo.filters import base_filter
from oeleo.movers import simple_mover
from oeleo.utils import calculate_checksum

log = logging.getLogger("oeleo")

FabricRunResult = Any
Hash = str


class Connector(Protocol):
    """Connectors are used to establish a connection to the server and
    provide the functions and methods needed for the movers and checkers.

    Connectors are typically only needed for transactions between computers.
    If no connector is given to the oeleo worker, the worker will use the
    same methods for local and external files.
    """

    directory = None

    def connect(self, **kwargs) -> None:
        ...

    def close(self) -> None:
        ...

    def base_filter_sub_method(
        self, glob_pattern: str = "*", **kwargs
    ) -> Union[list, Generator]:
        ...

    def calculate_checksum(self, f: Path, hide: bool = True) -> Hash:
        ...

    def move_func(self, path: Path, to: Path, *args, **kwargs) -> bool:
        ...


class LocalConnector(Connector):
    def __init__(self, directory=None):
        self.directory = directory or os.environ["OELEO_BASE_DIR_TO"]

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
    ) -> Generator[Path, None, None]:  # RENAME TO enquire
        return base_filter(self.directory, glob_pattern)

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
        self.directory = directory or os.environ["OELEO_BASE_DIR_TO"]
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
        else:
            self.directory = PureWindowsPath(self.directory)

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


def register_password(pwd: str = None) -> None:
    log.debug(" -> Register password ")
    if pwd is None:

        session_password = getpass.getpass(prompt="Password: ")
        os.environ["OELEO_PASSWORD"] = session_password
    log.debug(" Password registered!")
