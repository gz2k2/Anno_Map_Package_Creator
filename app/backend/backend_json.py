"""Safe JSON persistence with atomic replacement and schema preservation."""
from pathlib import Path
import json
import os
import tempfile

def read_json(path: Path, default):
    """Read JSON from path and return default when the file is missing."""
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def write_json_atomic(path: Path, payload) -> None:
    """Write JSON atomically so failed writes do not destroy valid data."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        Path(temporary).replace(path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise
