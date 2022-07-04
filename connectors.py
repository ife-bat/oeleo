import getpass
import logging
import os
from pathlib import Path, PurePosixPath
from typing import Any, Protocol

import dotenv
from fabric import Connection

# Playing around a bit to find out how to do ssh with python.

log = logging.getLogger("oeleo")

FabricRunResult = Any
Hash = str


class Connector(Protocol):
    """Connectors are used to establish a connection to the server and
    provide the functions and methods needed for the movers and checkers.
    """
    def connect(self, use_password: bool = False, **kwargs) -> None:
        ...

    def close(self, ):
        ...

    def base_filter_func(self, *args, **kwargs) -> list:
        ...

    def list_content(self, glob_pattern: str = "*", max_depth: int = 1, hide=False) -> FabricRunResult:
        ...

    def calculate_checksum(self, f: Path, hide: bool = True) -> Hash:
        ...

    def move_func(self, *args, **kwargs) -> str:
        ...


class SSHConnector(Connector):
    def __init__(self, username=None, host=None, directory=None, is_posix=True):
        self.session_password = os.environ["OELEO_PASSWORD"]
        self.username = username or os.environ["OELEO_USERNAME"]
        self.host = host or os.environ["EXTERNAL_TEST_HOST"]
        self.directory = directory or os.environ["BASE_DIR_TO"]
        self.is_posix = is_posix
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
            self.directory = Path(self.directory)

    def connect(self, use_password: bool = False, **kwargs) -> None:
        if use_password:
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

    def close(self):
        self.c.close()

    def __delete__(self, instance):
        if self.c is not None:
            self.c.close()

    def base_filter_func(self, glob_pattern="*") -> list:
        log.debug("base filter function for SSHConnector")
        log.debug("got this glob pattern:")
        log.debug(f"{glob_pattern}")

        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        result = self.list_content(glob_pattern, hide=True)
        file_list = result.stdout.strip().split("\n")
        if self.is_posix:
            file_list = [PurePosixPath(f) for f in file_list]
        else:
            file_list = [Path(f) for f in file_list]  # OBS Linux -> Win not supported!
        return file_list

    def list_content(self, glob_pattern="*", max_depth=1, hide=False):

        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        cmd = f"find {self.directory} -maxdepth {max_depth} -name '{glob_pattern}'"
        log.debug(cmd)
        result = self.c.run(cmd, hide=hide)
        if not result.ok:
            log.info("it failed - should raise an exception her (future work)")
        return result

    def calculate_checksum(self, f, hide=True):
        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        cmd = f"md5sum {self.directory/f}"
        result = self.c.run(cmd, hide=hide)
        if not result.ok:
            log.info("it failed - should raise an exception her (future work)")
        checksum = result.stdout.strip().split()[0]
        return checksum

    def move_func(self, path: Path, to: Path, **kwargs):
        if self.c is None:  # make this as a decorator ("@connected")
            log.debug("Connecting ...")
            self.connect()

        try:
            print(f"Copying {path} to {to}")
            result = self.c.put(str(path), remote=str(to))
        except Exception as e:
            print("GOT AN EXCEPTION DURING COPYING FILE")
            print(f"FROM     : {path}")
            print(f"TO       : {to}")
            print(f"EXCEPTION:")
            print(e)
            return False
        return True


def register_password(pwd: str = None) -> None:
    print(" Register password ".center(80, "="))
    if pwd is None:
        session_password = getpass.getpass(prompt="Password: ")
        os.environ["OELEO_PASSWORD"] = session_password
    print(" Done ".center(80, "="))


def main():
    dotenv.load_dotenv()
    local_dir = Path(r"C:\scripting\processing_cellpy\raw")

    external_dir = PurePosixPath("/home/jepe@ad.ife.no/Temp")
    external_host = os.environ["EXTERNAL_TEST_HOST"]
    username = os.environ["OELEO_USERNAME"]
    keyname = os.environ["OELEO_KEY_FILENAME"]
    password = os.environ["OELEO_PASSWORD"]

    register_password()
    session_password = os.environ["OELEO_PASSWORD"]
    c = Connection(
        host=external_host,
        user=username,
        connect_kwargs={
            "password": session_password,
            # "key_filename": [keyname],
        },
    )

    result = c.run(f"ls {external_dir}")
    print(result)


if __name__ == "__main__":
    main()
