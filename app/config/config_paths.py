"""Resolve writable and bundled paths in source and frozen builds."""
from pathlib import Path
import sys

def project_root() -> Path:
    """Return the source root or the directory containing the frozen executable."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]

def config_path() -> Path:
    """Return the root-level user configuration path."""
    return project_root() / "config.json"

def database_path(game: str) -> Path:
    """Return the database path for a supported game name."""
    filename = "anno_117.json" if game == "Anno 117" else "anno_1800.json"
    return project_root() / filename

def version_path() -> Path:
    """Return the local version file path."""
    return project_root() / "version.txt"
