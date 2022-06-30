import shutil
from pathlib import Path


def simple_mover(path: Path, to: Path):
    try:
        shutil.copyfile(path, to)
        return True
    except OSError:
        print("Could not copy this file - destination most likely not writable!")
        return False
