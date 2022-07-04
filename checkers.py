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
        return {"checksum": calculate_checksum(f)}


class ConnectedChecker(Checker):
    @staticmethod
    def check(f: Path, connector: Any = None, **kwargs) -> Dict[str, str]:
        """Calculates checksum using method provided by the connector"""
        if connector is not None:
            connector_calculate_checksum = connector.calculate_checksum
        else:
            connector_calculate_checksum = calculate_checksum

        return {"checksum": connector_calculate_checksum(f)}
