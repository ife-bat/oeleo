from pathlib import Path
from typing import Dict

from utils import calculate_checksum


class Checker:
    def __init__(self):
        pass

    def check(self, f: Path) -> Dict[str, str]:
        pass


class SimpleChecker(Checker):

    @staticmethod
    def check(f: Path) -> Dict[str, str]:
        """Calculates checksum and returns record key and"""
        return {"checksum": calculate_checksum(f)}
