"""Shared filesystem and metadata operations used by both game exporters."""
from pathlib import Path
import json
import re
import shutil
from app.models.model_export import ExportRequest, ExportResult, LogCallback
LANGUAGES = ('Chinese', 'English', 'French', 'German', 'Italian', 'Japanese', 'Korean', 'Polish', 'Russian', 'Spanish', 'Taiwanese')

def slug_component(value: str) -> str:
    """Convert a display value to a lowercase hyphen-separated ModID component."""
    normalized = re.sub('[^0-9a-z]+', '-', str(value).strip().lower())
    return normalized.strip('-')

def copy_map_folders(request: ExportRequest, log: LogCallback) -> tuple[int, int]:
    """Copy map folders into the package's game-region-specific islands directories.

    Each map is exported below ``data/<package-id>/<region-id>/islands``. The
    region directory uses the game-facing region ID stored in the map entry's
    resolved export mapping, for example ``moderate``, ``colony01``, or
    ``arctic``. Region IDs are passed in by the game-specific exporter because
    display-region translation belongs to that exporter.
    """
    region_maps = request.package.get("_export_region_ids", {})
    source_folders: list[tuple[Path, str]] = []
    seen_paths: set[tuple[str, str]] = set()

    for entry in request.entries:
        map_file = Path(entry.map_file)
        if not map_file.is_file():
            raise FileNotFoundError(f"Map file not found: {map_file}")

        region_id = str(region_maps.get(entry.region, "")).strip().lower()
        if not region_id:
            raise ValueError(f'No export Region ID is available for "{entry.region}".')

        key = (str(map_file.parent.resolve()).casefold(), region_id.casefold())
        if key not in seen_paths:
            seen_paths.add(key)
            source_folders.append((map_file.parent.resolve(), region_id))

    if request.target.exists():
        log(f"Removing existing folder: {request.target}")
        shutil.rmtree(request.target)

    used_destinations: set[tuple[str, str]] = set()
    copied_files = 0
    for source_folder, region_id in source_folders:
        destination_key = (region_id.casefold(), source_folder.name.casefold())
        if destination_key in used_destinations:
            raise ValueError(
                "Multiple map folders use the same folder name in region "
                f"{region_id}: {source_folder.name}"
            )
        used_destinations.add(destination_key)

        islands_root = request.target / "data" / request.package_id / region_id / "islands"
        islands_root.mkdir(parents=True, exist_ok=True)
        destination = islands_root / source_folder.name
        log(f"Copy folder: {source_folder} -> {destination}")

        for source in source_folder.rglob("*"):
            output = destination / source.relative_to(source_folder)
            if source.is_dir():
                output.mkdir(parents=True, exist_ok=True)
                continue
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, output)
            copied_files += 1
            log(f"Copied: {source} -> {output}")

    return len(source_folders), copied_files

def write_modinfo(request: ExportRequest, anno_value: int | None=None) -> Path:
    """Write the common modinfo.json structure with an optional Anno selector."""
    creator = str(request.settings.get('creator', '')).strip()
    creator_url = str(request.settings.get('creator_url', '')).strip()
    mod_name = str(request.package.get('mod_name', '')).strip()
    version = str(request.package.get('version', '')).strip()
    if not version:
        raise ValueError('Set Version in the Island Packages tab before exporting.')
    if not creator:
        raise ValueError('Set Creator in Settings > General before exporting.')

    # Build the payload with a ModID that is a combination of "mappackage", the slugified mod name, and the slugified creator name. The display name and description are prefixed with "[IslandPackage]". The payload includes version, Anno value (if provided), category, mod name, description, creator name, and contact information. The modinfo.json file is written to the target directory with UTF-8 encoding and proper formatting.
    # to add CreatorName and CreatorContact to the payload, we can include them in the dictionary as follows:
    # display_name = f'[IslandPackage] {mod_name} {creator}'
    # description = f'[IslandPackage] {mod_name} by {creator}'
    
    display_name = f'[IslandPackage] {mod_name}'
    description = f'[IslandPackage] {mod_name}'
    modio_game_id = '11358' if request.game == 'Anno 117' else '4169' if request.game == 'Anno 1800' else ''
    mod_name_slug = slug_component(mod_name)
    creator_slug = slug_component(creator)
    mod_id_parts = ['mappackage', mod_name_slug]
    if creator_slug and mod_name_slug != creator_slug and not mod_name_slug.endswith(f'-{creator_slug}'):
        mod_id_parts.append(creator_slug)
    payload = {'Version': version, 'ModID': '-'.join(filter(None, mod_id_parts)), 'modio_game_id': modio_game_id, 'modio_mod_id': str(request.package.get('modio_mod_id', '')).strip(), 'IncompatibleIds': [], 'LoadAfterIds': [], 'Category': {language: 'Map' for language in LANGUAGES}, 'ModName': {language: display_name for language in LANGUAGES}, 'Description': {language: description for language in LANGUAGES}, 'CreatorName': creator, 'CreatorContact': creator_url, 'Image': None}
    if anno_value is not None:
        payload = {'Version': version, 'Anno': anno_value, **{k: v for k, v in payload.items() if k != 'Version'}}
    path = request.target / 'modinfo.json'
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write('\n')
    return path

def finish_export(request: ExportRequest, log: LogCallback, copied: tuple[int, int]) -> ExportResult:
    """Create the value returned to the UI after game-specific files are written."""
    folders, files = copied
    log(f'Complete: {folders} folder(s), {files} file(s).')
    return ExportResult(request.target, folders, files)
