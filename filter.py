import hashlib
import shutil
from pathlib import Path
import os

import dotenv

dotenv.load_dotenv()
base_directory_from = Path(os.environ["BASE_DIR_FROM"])
base_directory_to = Path(os.environ["BASE_DIR_TO"])
filter_extension = os.environ["FILTER_EXTENSION"]


def filter_content(path: Path, extension: str = None) -> list:
    file_list = path.glob(f"*.{extension}")
    return file_list


def get_checksum_local_file(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def get_checksum_copied_file(file_path: Path) -> str:
    if file_path.is_file():
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()


def simple_mover(path: Path, to: Path):
    shutil.copyfile(path, to)


def check_if_updated(path: Path, old_checksum: str) -> bool:
    if get_checksum_local_file(path) != old_checksum:
        return True
    return False


if __name__ == "__main__":
    print(f"from: {base_directory_from}\nto: {base_directory_to}")

    filtered_list = filter_content(base_directory_from, filter_extension)
    print(filtered_list)
    for f in filtered_list:
        s = get_checksum_local_file(f)
        print(f.name)
        print(f"checksum type: {type(s)}, value: {s}")
        print("trying to copy file")
        simple_mover(f, base_directory_to / f.name)
