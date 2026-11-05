"""Central runtime path resolution for source and PyInstaller one-file modes. Writable application data remains next to the executable while bundled resources resolve from the PyInstaller extraction directory."""
from pathlib import Path
import sys

def root():
    """Return the writable application directory."""
    return Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parents[2]

def resource_root():
    """Return the directory containing bundled read-only resources."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]

def database_path(game):
    """Perform the database path operation for this module responsibility.

Args:
    game: Input used by the database path operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
    return root() / ('config_anno_117.json' if game == 'Anno 117' else 'config_anno_1800.json')

def config_path():
    """Perform the config path operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
    return root() / 'config.json'

def version_path():
    """Perform the version path operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
    return resource_root() / 'version.txt'
