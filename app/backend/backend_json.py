"""Low-level JSON persistence helpers. The module owns UTF-8 JSON loading and atomic replacement writes so callers do not duplicate persistence mechanics."""
import json, os, tempfile
from pathlib import Path

def read_json(path, default):
    """Perform the read json operation for this module responsibility.

Args:
    path: Input used by the read json operation.
    default: Input used by the read json operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
    if not path.exists():
        return default
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)

def write_json_atomic(path, payload):
    """Perform the write json atomic operation for this module responsibility.

Args:
    path: Input used by the write json atomic operation.
    payload: Input used by the write json atomic operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
    fd, tmp = tempfile.mkstemp(prefix=path.name, suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.write('\n')
        Path(tmp).replace(path)
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise
