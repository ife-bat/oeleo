from pathlib import Path


def filter_content(path: Path, extension: str = None) -> list:
    file_list = path.glob(f"*.{extension}")
    return file_list
