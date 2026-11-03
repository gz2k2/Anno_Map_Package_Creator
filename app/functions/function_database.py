from pathlib import Path
from app.backend.backend_json import read_json,write_json_atomic
from app.config.config_paths import database_path
from app.models.model_map_entry import MapEntry
from app.functions.function_settings import validate_guid_range
def load_entries(game):return [MapEntry.from_dict(x) for x in read_json(database_path(game),{"maps":[]}).get("maps",[])]
def save_entries(game,entries):
 payload=read_json(database_path(game),{});payload.update({"schema_version":1,"game":game,"maps":[e.to_dict() for e in entries]});write_json_atomic(database_path(game),payload)
def next_free_guid(entries,start,end):
 used={e.guid for e in entries}
 for guid in range(start,end+1):
  if guid not in used:return guid
 raise ValueError(f"No free GUID remains in range {start} to {end}.")
def import_map(game,file_path,start_text,end_text,update_duplicate=False):
 p=Path(file_path).resolve()
 if p.suffix.lower()!=".a7m":raise ValueError("Only .a7m files can be imported.")
 start,end=validate_guid_range(start_text,end_text);entries=load_entries(game);norm=str(p).casefold()
 duplicate=next((e for e in entries if str(Path(e.map_file)).casefold()==norm),None)
 if duplicate and not update_duplicate:return "duplicate",duplicate
 if duplicate:
  duplicate.map_name=p.stem;duplicate.map_file=str(p);save_entries(game,entries);return "updated",duplicate
 entry=MapEntry(p.stem,"","",next_free_guid(entries,start,end),"Normal",str(p));entries.append(entry);save_entries(game,entries);return "added",entry


def set_region(game, map_files, region):
 entries=load_entries(game); wanted={str(Path(x).resolve()).casefold() for x in map_files}; changed=0
 for entry in entries:
  if str(Path(entry.map_file).resolve()).casefold() in wanted:
   entry.region=region; changed+=1
 if changed: save_entries(game,entries)
 return changed


def delete_maps(game, map_files):
 entries=load_entries(game);wanted={str(Path(x).resolve()).casefold() for x in map_files};kept=[e for e in entries if str(Path(e.map_file).resolve()).casefold() not in wanted];deleted=len(entries)-len(kept)
 if deleted:save_entries(game,kept)
 return deleted

def assign_map_package(game,map_files,package):
 entries=load_entries(game);wanted={str(Path(x).resolve()).casefold() for x in map_files};changed=0
 for e in entries:
  if str(Path(e.map_file).resolve()).casefold() in wanted:e.map_package=package;changed+=1
 if changed:save_entries(game,entries)
 return changed

PACKAGE_ID_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"

def _package_id_from_index(index):
 if not 0 <= index < len(PACKAGE_ID_ALPHABET) ** 2:raise ValueError("No free two-character Map Package ID remains.")
 return PACKAGE_ID_ALPHABET[index // 36] + PACKAGE_ID_ALPHABET[index % 36]

def next_package_id(packages):
 used={str(x.get("id","")).lower() for x in packages if isinstance(x,dict) and len(str(x.get("id","")))==2}
 for index in range(36*36):
  candidate=_package_id_from_index(index)
  if candidate not in used:return candidate
 raise ValueError("No free two-character Map Package ID remains.")

def load_packages(game):
 raw=read_json(database_path(game),{"map_packages":[]}).get("map_packages",[])
 packages=[];changed=False
 for x in raw:
  if isinstance(x,str):pkg={"name":x,"mod_name":"","version":"","region":"","use_different_guid_ranges":False,"guid_start":"","guid_end":"","id":""};changed=True
  else:pkg={"name":str(x.get("name","")),"mod_name":str(x.get("mod_name","")),"version":str(x.get("version","")),"region":str(x.get("region","")),"use_different_guid_ranges":bool(x.get("use_different_guid_ranges",False)),"guid_start":str(x.get("guid_start","")),"guid_end":str(x.get("guid_end","")),"id":str(x.get("id","")).lower()}
  if len(pkg["id"])!=2 or any(c not in PACKAGE_ID_ALPHABET for c in pkg["id"]) or any(p["id"]==pkg["id"] for p in packages):pkg["id"]=next_package_id(packages);changed=True
  packages.append(pkg)
 if changed:save_packages(game,packages)
 return packages
def package_names(game):return [x["name"] for x in load_packages(game)]
def save_packages(game,packages):
 payload=read_json(database_path(game),{"schema_version":1,"game":game,"maps":[]});payload["map_packages"]=packages;write_json_atomic(database_path(game),payload)
def get_package(game,name):return next((x for x in load_packages(game) if x["name"]==name),None)
def add_package(game,name):
 name=name.strip();packages=load_packages(game)
 if not name:raise ValueError("Map Package name must not be empty.")
 if any(x["name"].casefold()==name.casefold() for x in packages):raise ValueError("This Map Package already exists.")
 packages.append({"name":name,"mod_name":"","version":"","region":"","use_different_guid_ranges":False,"guid_start":"","guid_end":"","id":next_package_id(packages)});save_packages(game,packages)
def rename_package(game,old,new):
 new=new.strip();packages=load_packages(game)
 if not new:raise ValueError("Map Package name must not be empty.")
 if any(x["name"].casefold()==new.casefold() and x["name"]!=old for x in packages):raise ValueError("This Map Package already exists.")
 for x in packages:
  if x["name"]==old:x["name"]=new
 save_packages(game,packages);entries=load_entries(game)
 for e in entries:
  if e.map_package==old:e.map_package=new
 save_entries(game,entries)
def delete_package(game,name):
 save_packages(game,[x for x in load_packages(game) if x["name"]!=name]);entries=load_entries(game)
 for e in entries:
  if e.map_package==name:e.map_package=""
 save_entries(game,entries)
def update_package_options(game,name,mod_name,version,region,use_range,guid_start,guid_end):
 packages=load_packages(game);pkg=next((x for x in packages if x["name"]==name),None)
 if not pkg:raise ValueError("Select a Map Package first.")
 if use_range:validate_guid_range(guid_start,guid_end)
 pkg.update({"mod_name":mod_name.strip(),"version":version.strip(),"region":region.strip(),"use_different_guid_ranges":bool(use_range),"guid_start":guid_start.strip(),"guid_end":guid_end.strip()});save_packages(game,packages)
def package_entries(game,name):return [e for e in load_entries(game) if e.map_package==name]
def apply_package_to_maps(game,map_files,package,apply_guids=False,apply_region=False):
 pkg=get_package(game,package)
 if not pkg:raise ValueError("Map Package no longer exists.")
 entries=load_entries(game);wanted={str(Path(x).resolve()).casefold() for x in map_files};targets=[e for e in entries if str(Path(e.map_file).resolve()).casefold() in wanted]
 for e in targets:e.map_package=package
 if apply_region and pkg["region"]:
  for e in targets:e.region=pkg["region"]
 if apply_guids and pkg["use_different_guid_ranges"]:
  start,end=validate_guid_range(pkg["guid_start"],pkg["guid_end"]);target_ids={id(e) for e in targets};used={e.guid for e in entries if id(e) not in target_ids};free=(x for x in range(start,end+1) if x not in used)
  for e in targets:
   try:e.guid=next(free)
   except StopIteration:raise ValueError(f"Not enough free GUIDs in Map Package range {start} to {end}.")
 save_entries(game,entries)

def remove_from_package(game, map_files):
 entries=load_entries(game);wanted={str(Path(x).resolve()).casefold() for x in map_files};changed=0
 for e in entries:
  if str(Path(e.map_file).resolve()).casefold() in wanted:
   e.map_package="";changed+=1
 if changed:save_entries(game,entries)
 return changed

def change_guid(game, map_file, new_guid_text):
 if not new_guid_text or not new_guid_text.isdigit():raise ValueError("GUID must contain digits only.")
 new_guid=int(new_guid_text);entries=load_entries(game);target=str(Path(map_file).resolve()).casefold();entry=next((e for e in entries if str(Path(e.map_file).resolve()).casefold()==target),None)
 if not entry:raise ValueError("Map entry was not found.")
 if any(e is not entry and e.guid==new_guid for e in entries):raise ValueError(f"GUID {new_guid} is already assigned to another map.")
 entry.guid=new_guid;save_entries(game,entries);return entry


def change_type(game, map_files, new_type):
 if new_type not in ("Normal","Decoration"):raise ValueError("Type must be Normal or Decoration.")
 entries=load_entries(game);wanted={str(Path(x).resolve()).casefold() for x in map_files};changed=0
 for entry in entries:
  if str(Path(entry.map_file).resolve()).casefold() in wanted:entry.map_type=new_type;changed+=1
 if changed:save_entries(game,entries)
 return changed
