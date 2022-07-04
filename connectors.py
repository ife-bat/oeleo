from pathlib import Path, PurePosixPath
import os
import dotenv
import getpass

from fabric import Connection

# Playing around a bit to find out how to do ssh with python.


class SSHConnector:

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

    def connect(self, use_password=False):
        if use_password:
            connect_kwargs = {
                "password": os.environ["OELEO_PASSWORD"],
            }
        else:
            connect_kwargs = {
                "key_filename": [os.environ["OELEO_KEY_FILENAME"]],
            }
        self.c = Connection(
            host=self.host,
            user=self.username,
            connect_kwargs=connect_kwargs
        )

    def list_content(self):
        cmd = f"ls {self.directory}"
        self.c.run(cmd)


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
        }
    )

    result = c.run(f"ls {external_dir}")
    print(result)


if __name__ == '__main__':
    main()
