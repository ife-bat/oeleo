import asyncio
import logging
import random
import shutil
import os
from pathlib import Path

log = logging.getLogger("oeleo")


def mock_mover(path: Path, to: Path, *args, **kwargs):
    print(f"COPYING {path} -> {to}")
    success = random.choice([True, False])
    print(f"success={success}")
    return success


def simple_recursive_mover(path: Path, to: Path, *args, **kwargs) -> bool:
    try:
        if path.is_dir():
            raise IOError("DIRECTORY")
        f_dir = to.parent
        if not f_dir.exists():
            os.makedirs(f_dir)
        shutil.copyfile(path, to)
        return True
    except OSError:
        log.debug(
            f"Could not copy {path.name} to directory {to.parent} - destination most likely not writable!"
        )
        return False


async def async_simple_recursive_mover(
    path: Path, to: Path, *args, **kwargs
) -> bool:
    """Async wrapper for simple_recursive_mover using a thread."""
    return await asyncio.to_thread(simple_recursive_mover, path, to, *args, **kwargs)


def simple_mover(path: Path, to: Path, *args, **kwargs) -> bool:
    try:
        shutil.copyfile(path, to)
        return True
    except OSError as e:
        print(f"Could not copy this file - {e}")
        log.debug("Could not copy this file - destination most likely not writable!")
        return False


async def async_simple_mover(path: Path, to: Path, *args, **kwargs) -> bool:
    """Async wrapper for simple_mover using a thread."""
    return await asyncio.to_thread(simple_mover, path, to, *args, **kwargs)


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


async def async_connected_mover(
    path: Path, to: Path, connector=None, *args, **kwargs
) -> bool:
    """Async wrapper for connected_mover using a thread."""
    return await asyncio.to_thread(connected_mover, path, to, connector, *args, **kwargs)
