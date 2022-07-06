from pathlib import Path
from typing import Any, Dict

from oeleo.utils import calculate_checksum


class Checker:
    def __init__(self):
        pass

    def check(self, f: Path) -> Dict[str, str]:  # UPDATE TYPES FOR ARGS
        pass


class ConnectedChecker(Checker):  # RENAME -> ChecksumChecker
    @staticmethod
    def check(f: Path, connector: Any = None, **kwargs) -> Dict[str, str]:
        """Calculates checksum using method provided by the connector"""
        if connector is not None:
            connector_calculate_checksum = connector.calculate_checksum
        else:
            connector_calculate_checksum = calculate_checksum

        return {"checksum": connector_calculate_checksum(f)}
