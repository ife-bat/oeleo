import logging
import random
import shutil
from pathlib import Path

log = logging.getLogger("oeleo")


def mock_mover(path: Path, to: Path, *args, **kwargs):
    print(f"COPYING {path} -> {to}")
    success = random.choice([True, False])
    print(f"success={success}")
    return success


def simple_mover(path: Path, to: Path, *args, **kwargs) -> bool:
    try:
        shutil.copyfile(path, to)
        return True
    except OSError:
        log.debug("Could not copy this file - destination most likely not writable!")
        return False


def connected_mover(path: Path, to: Path, connector=None, *args, **kwargs):
    """Copies files using the method implemented in the connector."""
    if connector is None:
        move_func = simple_mover
    else:
        move_func = connector.move_func
    try:
        success = move_func(path, to)
        return success
    except OSError:
        log.debug("Could not copy this file - destination most likely not writable!")
        return False
