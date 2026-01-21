from importlib.metadata import PackageNotFoundError, version


try:
    __version__ = version("oeleo")
except PackageNotFoundError:  # pragma: no cover - fallback for editable/uninstalled use
    __version__ = "0.0.0"

