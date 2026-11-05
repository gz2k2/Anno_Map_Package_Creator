"""Retrieve and compare local and remote application versions."""
from dataclasses import dataclass
from urllib.request import urlopen
from packaging.version import Version, InvalidVersion
from app.config.config_app import REMOTE_VERSION_URL
from app.config.config_paths import version_path

@dataclass(slots=True)
class UpdateResult:
    """Carry update state from the worker to the UI thread."""
    local: str
    remote: str | None
    state: str
    detail: str = ''

def check_for_update() -> UpdateResult:
    """Compare version.txt with the configured GitHub version file."""
    local = version_path().read_text(encoding='utf-8').strip()
    try:
        with urlopen(REMOTE_VERSION_URL, timeout=5) as response:
            remote = response.read().decode('utf-8').strip()
        state = 'update' if Version(remote) > Version(local) else 'current'
        return UpdateResult(local, remote, state)
    except (OSError, UnicodeError, InvalidVersion, ValueError) as exc:
        return UpdateResult(local, None, 'failed', str(exc))
