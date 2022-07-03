from pathlib import Path, PurePosixPath
import os
import dotenv

from fabric import Connection

# Playing around a bit to find out how to do ssh with python.

dotenv.load_dotenv()
local_dir = Path(r"C:\scripting\processing_cellpy\raw")


external_dir = PurePosixPath("/home/jepe@ad.ife.no/Temp")
external_host = os.environ["EXTERNAL_TEST_HOST"]
username = os.environ["USERNAME"]
keyname = os.environ["KEY_FILENAME"]


def main():
    c = Connection(
        host=external_host,
        user=username,
        connect_kwargs={
            "key_filename": [keyname],
        }
    )

    result = c.run(f"ls {external_dir}")
    print(result)


if __name__ == '__main__':
    main()