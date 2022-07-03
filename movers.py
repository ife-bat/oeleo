import random
import shutil
from pathlib import Path


def mock_mover(path: Path, to: Path):
    print(f"COPYING {path} -> {to}")
    success = random.choice([True, False])
    print(f"success={success}")
    return success


def simple_mover(path: Path, to: Path):
    try:
        shutil.copyfile(path, to)
        return True
    except OSError:
        print("Could not copy this file - destination most likely not writable!")
        return False
