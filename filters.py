from pathlib import Path
from typing import Generator


def filter_content(path: Path, extension: str = None) -> Generator[Path, None, None]:
    file_list = path.glob(f"*.{extension}")
    return file_list
