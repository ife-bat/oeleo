import hashlib
import shutil
from pathlib import Path
import os

import dotenv

from models import initialize_db, get_record_and_status, update
from filter import filter_content


def get_checksum_local_file(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def simple_mover(path: Path, to: Path):
    try:
        shutil.copyfile(path, to)
        return True
    except OSError:
        print("Could not copy this file - destination most likely not writable!")
        return False


class Watcher:
    """Checks if something has changed and triggers an event."""

    pass


class Filter:
    """Filters out the relevant files."""
    def __init__(self, filters):
        self.filters = filters


class Db:
    """Interacts with db."""


class Mover:
    """Moves the file."""

    pass


def main():
    dotenv.load_dotenv()
    base_directory_from = Path(os.environ["BASE_DIR_FROM"])
    base_directory_to = Path(os.environ["BASE_DIR_TO"])
    filter_extension = os.environ["FILTER_EXTENSION"]
    db = initialize_db(database_name=os.environ["DB_NAME"])

    print(f"from: {base_directory_from}\nto: {base_directory_to}")
    filtered_list = filter_content(base_directory_from, filter_extension)

    for f in filtered_list:
        checksum = get_checksum_local_file(f)
        record, needs_updating = get_record_and_status(f, checksum)
        if needs_updating:
            print(f" -> file has changed - need to copy")
            external_name = base_directory_to / f.name
            success = simple_mover(f, external_name)
            if success:
                print(f" -> succeeded in copying to {external_name}")
                update(record, external_name, checksum)


if __name__ == "__main__":
    main()
