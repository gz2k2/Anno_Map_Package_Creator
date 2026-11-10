"""Map and Map Package persistence operations. This module owns database-level validation, GUID allocation, package migration, assignments, and map metadata mutations without creating UI widgets."""
from pathlib import Path
from app.backend.backend_json import read_json, write_json_atomic
from app.config.config_paths import database_path
from app.models.model_map_entry import MapEntry
from app.functions.function_settings import validate_guid_range

def load_entries(game):
  """Perform the load entries operation for this module responsibility.

Args:
  game: Input used by the load entries operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  return [MapEntry.from_dict(x) for x in read_json(database_path(game), {'maps': []}).get('maps', [])]

def save_entries(game, entries):
  """Perform the save entries operation for this module responsibility.

Args:
  game: Input used by the save entries operation.
  entries: Input used by the save entries operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  payload = read_json(database_path(game), {})
  payload.update({'schema_version': 1, 'game': game, 'maps': [e.to_dict() for e in entries]})
  write_json_atomic(database_path(game), payload)

def next_free_guid(entries, start, end):
  """Perform the next free guid operation for this module responsibility.

Args:
  entries: Input used by the next free guid operation.
  start: Input used by the next free guid operation.
  end: Input used by the next free guid operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  used = {e.guid for e in entries}
  for guid in range(start, end + 1):
      if guid not in used:
          return guid
  raise ValueError(f'No free GUID remains in range {start} to {end}.')

def import_map(game, file_path, start_text, end_text, update_duplicate=False):
  """Perform the import map operation for this module responsibility.

Args:
  game: Input used by the import map operation.
  file_path: Input used by the import map operation.
  start_text: Input used by the import map operation.
  end_text: Input used by the import map operation.
  update_duplicate: Input used by the import map operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  p = Path(file_path).resolve()
  if p.suffix.lower() != '.a7m':
      raise ValueError('Only .a7m files can be imported.')
  start, end = validate_guid_range(start_text, end_text)
  entries = load_entries(game)
  norm = str(p).casefold()
  duplicate = next((e for e in entries if str(Path(e.map_file)).casefold() == norm), None)
  if duplicate and (not update_duplicate):
      return ('duplicate', duplicate)
  if duplicate:
      duplicate.map_name = p.stem
      duplicate.map_file = str(p)
      save_entries(game, entries)
      return ('updated', duplicate)
  entry = MapEntry(p.stem, '', '', next_free_guid(entries, start, end), 'Normal', str(p))
  entries.append(entry)
  save_entries(game, entries)
  return ('added', entry)

def set_region(game, map_files, region):
  """Perform the set region operation for this module responsibility.

Args:
  game: Input used by the set region operation.
  map_files: Input used by the set region operation.
  region: Input used by the set region operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  entries = load_entries(game)
  wanted = {str(Path(x).resolve()).casefold() for x in map_files}
  changed = 0
  for entry in entries:
      if str(Path(entry.map_file).resolve()).casefold() in wanted:
          entry.region = region
          changed += 1
  if changed:
      save_entries(game, entries)
  return changed

def delete_maps(game, map_files):
  """Perform the delete maps operation for this module responsibility.

Args:
  game: Input used by the delete maps operation.
  map_files: Input used by the delete maps operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  entries = load_entries(game)
  wanted = {str(Path(x).resolve()).casefold() for x in map_files}
  kept = [e for e in entries if str(Path(e.map_file).resolve()).casefold() not in wanted]
  deleted = len(entries) - len(kept)
  if deleted:
      save_entries(game, kept)
  return deleted

def assign_map_package(game, map_files, package):
  """Perform the assign map package operation for this module responsibility.

Args:
  game: Input used by the assign map package operation.
  map_files: Input used by the assign map package operation.
  package: Input used by the assign map package operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  entries = load_entries(game)
  wanted = {str(Path(x).resolve()).casefold() for x in map_files}
  changed = 0
  for e in entries:
      if str(Path(e.map_file).resolve()).casefold() in wanted:
          e.map_package = package
          changed += 1
  if changed:
      save_entries(game, entries)
  return changed
PACKAGE_ID_ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyz'

def _package_id_from_index(index):
  """Perform the package id from index operation for this module responsibility.

Args:
  index: Input used by the package id from index operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  if not 0 <= index < len(PACKAGE_ID_ALPHABET) ** 2:
      raise ValueError('No free two-character Map Package ID remains.')
  return PACKAGE_ID_ALPHABET[index // 36] + PACKAGE_ID_ALPHABET[index % 36]

def next_package_id(packages):
  """Perform the next package id operation for this module responsibility.

Args:
  packages: Input used by the next package id operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  used = {str(x.get('id', '')).lower() for x in packages if isinstance(x, dict) and len(str(x.get('id', ''))) == 2}
  for index in range(36 * 36):
      candidate = _package_id_from_index(index)
      if candidate not in used:
          return candidate
  raise ValueError('No free two-character Map Package ID remains.')

def load_packages(game):
  """Perform the load packages operation for this module responsibility.

Args:
  game: Input used by the load packages operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  raw = read_json(database_path(game), {'map_packages': []}).get('map_packages', [])
  packages = []
  changed = False
  for x in raw:
      if isinstance(x, str):
          pkg = {'name': x, 'mod_name': '', 'modio_mod_id': '', 'version': '', 'region': '', 'use_different_guid_ranges': False, 'guid_start': '', 'guid_end': '', 'id': '', 'additional_files': []}
          changed = True
      else:
          pkg = {'name': str(x.get('name', '')), 'mod_name': str(x.get('mod_name', '')), 'modio_mod_id': str(x.get('modio_mod_id', '')), 'version': str(x.get('version', '')), 'region': str(x.get('region', '')), 'use_different_guid_ranges': bool(x.get('use_different_guid_ranges', False)), 'guid_start': str(x.get('guid_start', '')), 'guid_end': str(x.get('guid_end', '')), 'id': str(x.get('id', '')).lower(), 'additional_files': [str(v) for v in x.get('additional_files', []) if str(v).strip()]}
      if len(pkg['id']) != 2 or any((c not in PACKAGE_ID_ALPHABET for c in pkg['id'])) or any((p['id'] == pkg['id'] for p in packages)):
          pkg['id'] = next_package_id(packages)
          changed = True
      packages.append(pkg)
  if changed:
      save_packages(game, packages)
  return packages

def package_names(game):
  """Perform the package names operation for this module responsibility.

Args:
  game: Input used by the package names operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  return [x['name'] for x in load_packages(game)]

def save_packages(game, packages):
  """Perform the save packages operation for this module responsibility.

Args:
  game: Input used by the save packages operation.
  packages: Input used by the save packages operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  payload = read_json(database_path(game), {'schema_version': 1, 'game': game, 'maps': []})
  payload['map_packages'] = packages
  write_json_atomic(database_path(game), payload)

def get_package(game, name):
  """Perform the get package operation for this module responsibility.

Args:
  game: Input used by the get package operation.
  name: Input used by the get package operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  return next((x for x in load_packages(game) if x['name'] == name), None)

def add_package(game, name):
  """Perform the add package operation for this module responsibility.

Args:
  game: Input used by the add package operation.
  name: Input used by the add package operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  name = name.strip()
  packages = load_packages(game)
  if not name:
      raise ValueError('Map Package name must not be empty.')
  if any((x['name'].casefold() == name.casefold() for x in packages)):
      raise ValueError('This Map Package already exists.')
  packages.append({'name': name, 'mod_name': '', 'modio_mod_id': '', 'version': '', 'region': '', 'use_different_guid_ranges': False, 'guid_start': '', 'guid_end': '', 'id': next_package_id(packages), 'additional_files': []})
  save_packages(game, packages)

def update_package_additional_files(game, name, folders):
  """Perform the update package additional files operation for this module responsibility.

Args:
  game: Input used by the update package additional files operation.
  name: Input used by the update package additional files operation.
  folders: Input used by the update package additional files operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  packages = load_packages(game)
  pkg = next((x for x in packages if x['name'] == name), None)
  if not pkg:
      raise ValueError('Select a Map Package first.')
  pkg['additional_files'] = [str(Path(folder)) for folder in folders]
  save_packages(game, packages)

def rename_package(game, old, new):
  """Perform the rename package operation for this module responsibility.

Args:
  game: Input used by the rename package operation.
  old: Input used by the rename package operation.
  new: Input used by the rename package operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  new = new.strip()
  packages = load_packages(game)
  if not new:
      raise ValueError('Map Package name must not be empty.')
  if any((x['name'].casefold() == new.casefold() and x['name'] != old for x in packages)):
      raise ValueError('This Map Package already exists.')
  for x in packages:
      if x['name'] == old:
          x['name'] = new
  save_packages(game, packages)
  entries = load_entries(game)
  for e in entries:
      if e.map_package == old:
          e.map_package = new
  save_entries(game, entries)

def delete_package(game, name):
  """Perform the delete package operation for this module responsibility.

Args:
  game: Input used by the delete package operation.
  name: Input used by the delete package operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  save_packages(game, [x for x in load_packages(game) if x['name'] != name])
  entries = load_entries(game)
  for e in entries:
      if e.map_package == name:
          e.map_package = ''
  save_entries(game, entries)

def update_package_options(game, name, mod_name, version, region, use_range, guid_start, guid_end, modio_mod_id=''):
  """Perform the update package options operation for this module responsibility.

Args:
  game: Input used by the update package options operation.
  name: Input used by the update package options operation.
  mod_name: Input used by the update package options operation.
  version: Input used by the update package options operation.
  region: Input used by the update package options operation.
  use_range: Input used by the update package options operation.
  guid_start: Input used by the update package options operation.
  guid_end: Input used by the update package options operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  packages = load_packages(game)
  pkg = next((x for x in packages if x['name'] == name), None)
  if not pkg:
      raise ValueError('Select a Map Package first.')
  if use_range:
      validate_guid_range(guid_start, guid_end)
  pkg.update({'mod_name': mod_name.strip(), 'modio_mod_id': str(modio_mod_id).strip(), 'version': version.strip(), 'region': region.strip(), 'use_different_guid_ranges': bool(use_range), 'guid_start': guid_start.strip(), 'guid_end': guid_end.strip()})
  save_packages(game, packages)

def package_entries(game, name):
  """Perform the package entries operation for this module responsibility.

Args:
  game: Input used by the package entries operation.
  name: Input used by the package entries operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  return [e for e in load_entries(game) if e.map_package == name]

def apply_package_to_maps(game, map_files, package, apply_guids=False, apply_region=False):
  """Perform the apply package to maps operation for this module responsibility.

Args:
  game: Input used by the apply package to maps operation.
  map_files: Input used by the apply package to maps operation.
  package: Input used by the apply package to maps operation.
  apply_guids: Input used by the apply package to maps operation.
  apply_region: Input used by the apply package to maps operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  pkg = get_package(game, package)
  if not pkg:
      raise ValueError('Map Package no longer exists.')
  entries = load_entries(game)
  wanted = {str(Path(x).resolve()).casefold() for x in map_files}
  targets = [e for e in entries if str(Path(e.map_file).resolve()).casefold() in wanted]
  for e in targets:
      e.map_package = package
  if apply_region and pkg['region']:
      for e in targets:
          e.region = pkg['region']
  if apply_guids and pkg['use_different_guid_ranges']:
      start, end = validate_guid_range(pkg['guid_start'], pkg['guid_end'])
      target_ids = {id(e) for e in targets}
      used = {e.guid for e in entries if id(e) not in target_ids}
      free = (x for x in range(start, end + 1) if x not in used)
      for e in targets:
          try:
              e.guid = next(free)
          except StopIteration:
              raise ValueError(f'Not enough free GUIDs in Map Package range {start} to {end}.')
  save_entries(game, entries)

def reassign_unassigned_guids(game, guid_start, guid_end):
  """Reassign GUIDs only for maps that are not assigned to any Map Package.

  The General-tab GUID range is used as the allocation pool. GUIDs currently
  used by packaged maps are reserved and skipped. The operation validates
  capacity before changing any entry so a too-small range cannot leave a
  partially reassigned database.
  """
  start, end = validate_guid_range(guid_start, guid_end)
  entries = load_entries(game)
  targets = [entry for entry in entries if not str(entry.map_package).strip()]
  reserved = {entry.guid for entry in entries if str(entry.map_package).strip()}
  available = [guid for guid in range(start, end + 1) if guid not in reserved]
  if len(available) < len(targets):
      raise ValueError(
          f"Not enough free GUIDs in General GUID range {start} to {end}. "
          f"Required: {len(targets)}, available: {len(available)}."
      )
  for entry, guid in zip(targets, available):
      entry.guid = guid
  if targets:
      save_entries(game, entries)
  return len(targets)

def reassign_package_guids(game, package_name):
  """Reassign all GUIDs of a Map Package from its configured GUID range.

  GUIDs are assigned sequentially in the current package table order. GUIDs
  already used by maps outside the current package are skipped to preserve
  global uniqueness. The operation is atomic: no entry is saved unless the
  configured range can accommodate every map in the package.

  Args:
      game: Selected game database.
      package_name: Name of the Map Package whose GUIDs must be reassigned.

  Returns:
      Number of Map Package entries that received a new GUID.

  Raises:
      ValueError: If the package is missing, range mode is disabled, the
          range is invalid, or too few free GUIDs are available.
  """
  pkg = get_package(game, package_name)
  if not pkg:
      raise ValueError("Select a valid Map Package first.")
  if not pkg.get("use_different_guid_ranges"):
      raise ValueError("Use different GUID ranges must be enabled first.")

  start, end = validate_guid_range(pkg.get("guid_start", ""), pkg.get("guid_end", ""))
  entries = load_entries(game)
  targets = [entry for entry in entries if entry.map_package == package_name]
  target_ids = {id(entry) for entry in targets}
  used_outside_package = {entry.guid for entry in entries if id(entry) not in target_ids}
  available = [guid for guid in range(start, end + 1) if guid not in used_outside_package]

  if len(available) < len(targets):
      raise ValueError(
          f"Not enough free GUIDs in Map Package range {start} to {end}. "
          f"Required: {len(targets)}, available: {len(available)}."
      )

  for entry, guid in zip(targets, available):
      entry.guid = guid

  if targets:
      save_entries(game, entries)
  return len(targets)

def remove_from_package(game, map_files):
  """Perform the remove from package operation for this module responsibility.

Args:
  game: Input used by the remove from package operation.
  map_files: Input used by the remove from package operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  entries = load_entries(game)
  wanted = {str(Path(x).resolve()).casefold() for x in map_files}
  changed = 0
  for e in entries:
      if str(Path(e.map_file).resolve()).casefold() in wanted:
          e.map_package = ''
          changed += 1
  if changed:
      save_entries(game, entries)
  return changed

def change_guid(game, map_file, new_guid_text):
  """Perform the change guid operation for this module responsibility.

Args:
  game: Input used by the change guid operation.
  map_file: Input used by the change guid operation.
  new_guid_text: Input used by the change guid operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  if not new_guid_text or not new_guid_text.isdigit():
      raise ValueError('GUID must contain digits only.')
  new_guid = int(new_guid_text)
  entries = load_entries(game)
  target = str(Path(map_file).resolve()).casefold()
  entry = next((e for e in entries if str(Path(e.map_file).resolve()).casefold() == target), None)
  if not entry:
      raise ValueError('Map entry was not found.')
  if any((e is not entry and e.guid == new_guid for e in entries)):
      raise ValueError(f'GUID {new_guid} is already assigned to another map.')
  entry.guid = new_guid
  save_entries(game, entries)
  return entry

def change_type(game, map_files, new_type):
  """Perform the change type operation for this module responsibility.

Args:
  game: Input used by the change type operation.
  map_files: Input used by the change type operation.
  new_type: Input used by the change type operation.

Returns:
  The operation result when one is produced; otherwise None.

Side effects:
  May update application state, persistent data, filesystem content, or UI state as implied by the owning module."""
  if new_type not in ('Normal', 'Decoration', 'Starter'):
      raise ValueError('Type must be Normal, Decoration, or Starter.')
  entries = load_entries(game)
  wanted = {str(Path(x).resolve()).casefold() for x in map_files}
  changed = 0
  for entry in entries:
      if str(Path(entry.map_file).resolve()).casefold() in wanted:
          entry.map_type = new_type
          changed += 1
  if changed:
      save_entries(game, entries)
  return changed

def change_island_size(game, map_files, new_size):
    """Set the explicit Anno 117 island placeholder size for selected maps."""
    if game != 'Anno 117':
        raise ValueError('Island Size is only available for Anno 117.')
    if new_size not in ('Auto', 'Medium', 'Large', 'XL'):
        raise ValueError('Island Size must be Auto, Medium, Large, or XL.')
    entries = load_entries(game)
    wanted = {str(Path(x).resolve()).casefold() for x in map_files}
    changed = 0
    for entry in entries:
        if str(Path(entry.map_file).resolve()).casefold() in wanted:
            entry.island_size = new_size
            changed += 1
    if changed:
        save_entries(game, entries)
    return changed
