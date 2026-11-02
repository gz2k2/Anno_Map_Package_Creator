"""Typed model for one map database row."""
from dataclasses import dataclass

@dataclass(slots=True)
class MapEntry:
    """Represent one map package database entry."""
    map_name: str
    region: str
    map_package: str
    guid: int
    map_file: str

    @classmethod
    def from_dict(cls, value: dict) -> "MapEntry":
        """Create a validated entry from JSON-compatible data."""
        return cls(str(value.get("Map_Name", "")), str(value.get("Region", "")), str(value.get("Map_Package", "")), int(value.get("GUID", 0)), str(value.get("Map_File", "")))

    def to_dict(self) -> dict:
        """Convert the entry to the public database schema."""
        return {"Map_Name": self.map_name, "Region": self.region, "Map_Package": self.map_package, "GUID": self.guid, "Map_File": self.map_file}
