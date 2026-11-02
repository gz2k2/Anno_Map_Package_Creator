"""Read map entries for the selected Anno game database."""
from app.backend.backend_json import read_json
from app.config.config_paths import database_path
from app.models.model_map_entry import MapEntry

def load_entries(game: str) -> list[MapEntry]:
    """Load and validate all entries for one game."""
    payload = read_json(database_path(game), {"maps": []})
    return [MapEntry.from_dict(item) for item in payload.get("maps", [])]
