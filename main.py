import os
from pathlib import Path

import dotenv

from filters import filter_content
from models import get_record_and_status, initialize_db, update
from movers import simple_mover
from utils import calculate_checksum


def main():
    dotenv.load_dotenv()
    base_directory_from = Path(os.environ["BASE_DIR_FROM"])
    base_directory_to = Path(os.environ["BASE_DIR_TO"])
    filter_extension = os.environ["FILTER_EXTENSION"]
    db = initialize_db(database_name=os.environ["DB_NAME"])

    print(f"from: {base_directory_from}\nto: {base_directory_to}")
    filtered_list = filter_content(base_directory_from, filter_extension)

    for f in filtered_list:
        checksum = calculate_checksum(f)
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
