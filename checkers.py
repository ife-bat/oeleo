from pathlib import Path
from typing import Any, Dict

from utils import calculate_checksum


class Checker:
    def __init__(self):
        pass

    def check(self, f: Path) -> Dict[str, str]:
        pass


class SimpleChecker(Checker):
    @staticmethod
    def check(f: Path, **kwargs) -> Dict[str, str]:
        """Calculates checksum and returns record key and"""
        return {"checksum": calculate_checksum(f)}


class ConnectedChecker(Checker):
    @staticmethod
    def check(
        f: Path, connector: Any = None, **kwargs
    ) -> Dict[str, str]:
        if connector is not None:
            connector_calculate_checksum = connector.calculate_checksum
        else:
            connector_calculate_checksum = calculate_checksum
        """Calculates checksum and returns record key and"""
        return {"checksum": connector_calculate_checksum(f)}
