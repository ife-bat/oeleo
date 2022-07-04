import random
import shutil
from pathlib import Path


def mock_mover(path: Path, to: Path):
    print(f"COPYING {path} -> {to}")
    success = random.choice([True, False])
    print(f"success={success}")
    return success


def simple_mover(path: Path, to: Path, **kwargs):
    try:
        shutil.copyfile(path, to)
        return True
    except OSError:
        print("Could not copy this file - destination most likely not writable!")
        return False


def connected_mover(path: Path, to: Path, connector=None, *args, **kwargs):
    if connector is None:
        move_func = simple_mover
    else:
        move_func = connector.move_func
    try:
        success = move_func(path, to)
        return success
    except OSError:
        print("Could not copy this file - destination most likely not writable!")
        return False

