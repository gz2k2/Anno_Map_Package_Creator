"""Built-in regions, separated by supported game and carrying their game-specific IDs."""

FIXED_REGIONS = {
    "Anno 117": (
        {"region": "Albion", "id": "Celtic"},
        {"region": "Latium", "id": "Roman"},
    ),
    "Anno 1800": (
        {"region": "Arctic", "id": "Arctic"},
        {"region": "Enbesa", "id": "Africa"},
        {"region": "The New World", "id": "Colony01"},
        {"region": "The Old World", "id": "Moderate"},
    ),
}


def get_fixed_regions(game: str) -> list[dict[str, str]]:
    """Return fixed region records for the selected game, sorted by display name."""
    return sorted((dict(item) for item in FIXED_REGIONS.get(game, ())), key=lambda item: item["region"].casefold())
