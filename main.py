import os
from dataclasses import dataclass, field
import time
from pathlib import Path
from typing import Any, Generator

import dotenv
from rich.progress import Progress

from filters import filter_content
from models import SimpleDbHandler, DbHandler
from movers import simple_mover
from utils import calculate_checksum


@dataclass
class Worker:
    filter_method: Any
    checker_method: Any
    mover_method: Any
    from_dir: Path
    to_dir: Path
    bookkeeper: DbHandler
    file_names: Generator[Path, None, None] = field(init=False)

    def connect_to_db(self):
        print("...Connecting to db")
        self.bookkeeper.initialize_db()
        print(f" -> {self.bookkeeper.db_name}")

    def filter(self, *args, **kwargs):
        print("...Filtering")
        """ Update the db """
        self.file_names = self.filter_method(
            self.from_dir,
            *args, **kwargs,
        )

    def check(self):
        """ Check for differences between the two directories. """
        pass

    def run(self):
        """ Copy the files that needs to be copied and update the db. """
        with Progress() as progress:
            for f in self.file_names:
                task_id = progress.add_task(f"{f.name} processing")
                progress.update(task_id, advance=10, description=f"{f.name} calculate checksum")
                checksum = calculate_checksum(f)
                progress.update(task_id, advance=10, description=f"{f.name} registering")
                self.bookkeeper.register(f)
                if self.bookkeeper.is_changed(checksum):
                    status = ":bow_and_arrow:"
                    external_name = self.to_dir / f.name
                    progress.update(task_id, advance=10, description=f"{f.name} copying")
                    success = self.mover_method(f, external_name)
                    if success:
                        progress.update(task_id, advance=10, description=f"{f.name} updating")
                        self.bookkeeper.update_record(external_name, checksum)
                        status += ":thumbs_up:"
                    else:
                        status += ":thumbs_down:"
                else:
                    status = ":sleeping_face:"
                    progress.update(task_id, advance=100)
                progress.update(task_id, advance=100, description=f"{f.name} {status}")


def main():
    dotenv.load_dotenv()

    bookkeeper = SimpleDbHandler(os.environ["DB_NAME"])

    base_directory_from = Path(os.environ["BASE_DIR_FROM"])
    base_directory_to = Path(os.environ["BASE_DIR_TO"])
    filter_extension = os.environ["FILTER_EXTENSION"]

    worker = Worker(
        filter_method=filter_content,
        checker_method=None,
        mover_method=simple_mover,
        from_dir=base_directory_from,
        to_dir=base_directory_to,
        bookkeeper=bookkeeper,
    )

    worker.connect_to_db()
    worker.filter(filter_extension)
    worker.check()
    worker.run()


if __name__ == "__main__":
    main()
