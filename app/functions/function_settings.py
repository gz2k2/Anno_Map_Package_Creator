"""Load, validate, and save application settings."""
from app.backend.backend_json import read_json, write_json_atomic
from app.config.config_app import DEFAULT_GAME, DEFAULT_WORKER_COUNT, SUPPORTED_GAMES
from app.config.config_paths import config_path

DEFAULT_SETTINGS = {"selected_game": DEFAULT_GAME, "worker_count": DEFAULT_WORKER_COUNT, "games": {game: {"guid_start": "", "guid_end": ""} for game in SUPPORTED_GAMES}}

def load_settings() -> dict:
    """Load settings and merge missing keys with current defaults."""
    saved = read_json(config_path(), {})
    result = {"selected_game": saved.get("selected_game", DEFAULT_GAME), "worker_count": saved.get("worker_count", DEFAULT_WORKER_COUNT), "games": {}}
    for game in SUPPORTED_GAMES:
        result["games"][game] = {**DEFAULT_SETTINGS["games"][game], **saved.get("games", {}).get(game, {})}
    return result

def validate_guid_range(start: str, end: str) -> tuple[int|None, int|None]:
    """Validate optional numeric GUID boundaries and their order."""
    if start and not start.isdigit() or end and not end.isdigit():
        raise ValueError("GUID values may contain digits only.")
    low, high = (int(start) if start else None), (int(end) if end else None)
    if low is not None and high is not None and low > high:
        raise ValueError("GUID Start must not be greater than GUID End.")
    return low, high

def save_settings(settings: dict) -> None:
    """Validate and atomically persist application settings."""
    for game in SUPPORTED_GAMES:
        values = settings["games"][game]
        validate_guid_range(values["guid_start"], values["guid_end"])
    workers = int(settings["worker_count"])
    if not 1 <= workers <= 32:
        raise ValueError("Worker count must be between 1 and 32.")
    write_json_atomic(config_path(), settings)
