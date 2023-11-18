import logging
from datetime import datetime
from functools import partial
import os
from pathlib import Path
from typing import Any, Generator, Iterable, Union, Callable

log = logging.getLogger("oeleo")


def filter_on_startswith(path: Union[Path, str], value: str):
    return os.path.basename(path).startswith(value)


def filter_on_contains(path: Union[Path, str], value: str):
    return value in os.path.basename(path)


def filter_on_not_contains(path: Union[Path, str], value: str):
    return value not in os.path.basename(path)


def filter_on_callable(path: Union[Path, str], f: Callable):
    return f(os.path.basename(path))


def filter_on_not_before(path: Union[Path, str], value: datetime):
    st = os.stat(path)
    sdt = datetime.fromtimestamp(st.st_mtime)
    if sdt >= value:
        return True
    else:
        return False


def filter_on_not_after(path: Union[Path, str], value: datetime):
    st = os.stat(path)
    sdt = datetime.fromtimestamp(st.st_mtime)
    if sdt <= value:
        return True
    else:
        return False


FILTERS = {
    "startswith": filter_on_startswith,
    "contains": filter_on_contains,
    "callable": filter_on_callable,
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

    """Simple directory content filter - cannot be used for ssh"""

    if base_filter_func is None:
        base_filter_func = path.glob

    file_list = base_filter_func(f"*{extension}")

    if additional_filters is not None:
        file_list = additional_filtering(file_list, additional_filters)

    return file_list


def additional_filtering(
    file_list: Iterable[Union[Path, str]],
    additional_filters: Iterable[FilterTuple] = None,
) -> Iterable:
    for filter_name, filter_val in additional_filters:
        filter_func = FILTERS[filter_name]
        file_list = filter(partial(filter_func, value=filter_val), file_list)
    return file_list


def main():
    directory = Path("../check/from").resolve()
    not_before = datetime(year=2022, month=7, day=1, hour=1, minute=0, second=0)
    not_after = datetime(year=2022, month=8, day=4, hour=1, minute=0, second=0)
    print(f"not_before: {not_before}")
    print(f"not_after: {not_after}")
    for f in directory.glob("*"):
        print(f"file: {f}: {datetime.fromtimestamp(f.stat().st_mtime)}")
    extension = ".xyz"

    print("Starting...")

    my_filters = [
        ("not_before", not_before),
        ("not_after", not_after),
    ]

    g = base_filter(directory, extension, additional_filters=my_filters)
    print("This is what I got after filtering:")
    for n, f in enumerate(g):
        st_mtime = datetime.fromtimestamp(f.stat().st_mtime)
        print(
            f"{n+1}: {f} {st_mtime} not-before: {st_mtime >= not_before} not-after: {st_mtime <= not_after}"
        )


if __name__ == "__main__":
    main()
