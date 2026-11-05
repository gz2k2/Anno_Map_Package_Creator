"""Typed contracts used by the map-export services and the export UI worker."""
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
LogCallback = Callable[[str], None]

@dataclass(frozen=True, slots=True)
class ExportRequest:
    """Describe one immutable map-package export operation."""
    game: str
    target: Path
    package_id: str
    package: dict
    entries: tuple
    settings: dict

@dataclass(frozen=True, slots=True)
class ExportResult:
    """Summarize a completed export for display by the UI layer."""
    target: Path
    copied_folders: int
    copied_files: int
