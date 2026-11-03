"""Shared filesystem and metadata operations used by both game exporters."""
from pathlib import Path
import json
import re
import shutil

from app.models.model_export import ExportRequest, ExportResult, LogCallback

LANGUAGES = (
    "Chinese", "English", "French", "German", "Italian", "Japanese",
    "Korean", "Polish", "Russian", "Spanish", "Taiwanese",
)


def slug_component(value: str) -> str:
    """Convert a display value to a lowercase hyphen-separated ModID component."""
    normalized = re.sub(r"[^0-9a-z]+", "-", str(value).strip().lower())
    return normalized.strip("-")


def copy_map_folders(request: ExportRequest, log: LogCallback) -> tuple[int, int]:
    """Copy each unique map source folder into data/<package-id>/islands."""
    source_folders: list[Path] = []
    seen_paths: set[str] = set()
    for entry in request.entries:
        map_file = Path(entry.map_file)
        if not map_file.is_file():
            raise FileNotFoundError(f"Map file not found: {map_file}")
        key = str(map_file.parent.resolve()).casefold()
        if key not in seen_paths:
            seen_paths.add(key)
            source_folders.append(map_file.parent.resolve())

    if request.target.exists():
        log(f"Removing existing folder: {request.target}")
        shutil.rmtree(request.target)

    islands_root = request.target / "data" / request.package_id / "islands"
    islands_root.mkdir(parents=True)
    log(f"Islands folder: {islands_root}")

    used_names: set[str] = set()
    copied_files = 0
    for source_folder in source_folders:
        folder_key = source_folder.name.casefold()
        if folder_key in used_names:
            raise ValueError(f"Multiple map folders use the same folder name: {source_folder.name}")
        used_names.add(folder_key)
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


def write_modinfo(request: ExportRequest, anno_value: int | None = None) -> Path:
    """Write the common modinfo.json structure with an optional Anno selector."""
    creator = str(request.settings.get("creator", "")).strip()
    creator_url = str(request.settings.get("creator_url", "")).strip()
    mod_name = str(request.package.get("mod_name", "")).strip()
    version = str(request.package.get("version", "")).strip()
    if not version:
        raise ValueError("Set Version in the Map Packages tab before exporting.")
    if not creator:
        raise ValueError("Set Creator in Settings > General before exporting.")
    display_name = f"[MapPackage] {mod_name} [{creator}]"
    description = f"[MapPackage] {mod_name}"
    payload = {
        "Version": version,
        "ModID": "-".join(filter(None, ("mappackage", slug_component(mod_name), slug_component(creator)))),
        "IncompatibleIds": [],
        "LoadAfterIds": [],
        "Category": {language: "Map" for language in LANGUAGES},
        "ModName": {language: display_name for language in LANGUAGES},
        "Description": {language: description for language in LANGUAGES},
        "CreatorName": creator,
        "CreatorContact": creator_url,
        "Image": None,
    }
    if anno_value is not None:
        payload = {"Version": version, "Anno": anno_value, **{k: v for k, v in payload.items() if k != "Version"}}
    path = request.target / "modinfo.json"
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return path


def finish_export(request: ExportRequest, log: LogCallback, copied: tuple[int, int]) -> ExportResult:
    """Create the value returned to the UI after game-specific files are written."""
    folders, files = copied
    log(f"Complete: {folders} folder(s), {files} file(s).")
    return ExportResult(request.target, folders, files)
