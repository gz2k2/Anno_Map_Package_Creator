# Changelog

## 1.0.1

### Added

- Added **Reassign GUIDs** to the General tab. It reassigns GUIDs only for maps without a Map Package and uses the active game's General GUID range.
- Added **Reassign GUIDs** to the Map Packages tab when **Use different GUID ranges** is enabled. It reassigns all GUIDs in the current package from the package-specific range.
- Added **Remove from Package** to the General-tab right-click menu with multi-selection support.

### Changed

- GUID reassignment validates the complete available range before saving, preventing partial changes.
- Package and General GUID reassignment reserve GUIDs belonging to entries outside the affected scope.
- Updated the General-tab and Map Packages context-menu documentation.
- Changed map export paths to include the resolved Region ID below the Package ID: `data/<Package ID>/<Region ID>/islands/...` (for example `data/00/moderate/islands/...` or `data/00/arctic/islands/...`). Generated `assets.xml` paths now follow the same structure.

