"""Typed map-entry model used by database and UI layers. It owns conversion between in-memory map fields and the established JSON schema."""
from dataclasses import dataclass

@dataclass(slots=True)
class MapEntry:
    """Represent the MapEntry component and own its lifecycle within this module."""
    map_name: str
    region: str
    map_package: str
    guid: int
    map_type: str
    map_file: str

    @classmethod
    def from_dict(cls, v):
        """Perform the from dict operation for this module responsibility.

Args:
    v: Input used by the from dict operation.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        return cls(str(v.get('Map_Name', '')), str(v.get('Region', '')), str(v.get('Map_Package', '')), int(v.get('GUID', 0)), str(v.get('Type', 'Normal')), str(v.get('Map_File', '')))

    def to_dict(self):
        """Perform the to dict operation for this module responsibility.

Returns:
    The operation result when one is produced; otherwise None.

Side effects:
    May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
        return {'Map_Name': self.map_name, 'Region': self.region, 'Map_Package': self.map_package, 'GUID': self.guid, 'Type': self.map_type, 'Map_File': self.map_file}
