import logging
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Generator, Iterable

log = logging.getLogger(__name__)


def filter_on_not_before(path: Path, value: datetime):
    st = path.stat()
    sdt = datetime.fromtimestamp(st.st_mtime)
    if sdt >= value:
        return True
    else:
        return False


def filter_on_not_after(path: Path, value: datetime):
    st = path.stat()
    sdt = datetime.fromtimestamp(st.st_mtime)
    if sdt <= value:
        return True
    else:
        return False


FILTERS = {
    "not_before": filter_on_not_before,
    "not_after": filter_on_not_after,
}

FilterFunction = Any
FilterTuple = Any  # tuple[str, FilterFunction] for py3.10


def base_filter(
    path: Path,
    extension: str = None,
    additional_filters: Iterable[FilterTuple] = None,
    base_filter_func: Any = None,
) -> Generator[Path, None, None]:

    """Simple directory content filter - cannot be used for ssh (yet)?"""

    if base_filter_func is None:
        base_filter_func = path.glob

    file_list = base_filter_func(f"*{extension}")
    if additional_filters is not None:
        for filter_name, filter_val in additional_filters:
            filter_func = FILTERS[filter_name]
            file_list = filter(partial(filter_func, value=filter_val), file_list)

    return file_list


def main():
    directory = Path(r"/check/from")
    extension = "*"
    not_before = datetime(year=2022, month=7, day=1, hour=1, minute=0, second=0)
    not_after = datetime(year=2022, month=7, day=4, hour=1, minute=0, second=0)
    print("Starting...")

    my_filters = [
        ("not_before", not_before),
        ("not_after", not_after),
    ]

    g = base_filter(directory, extension, additional_filters=my_filters)
    for i in g:
        print(i)


if __name__ == "__main__":
    main()
