from app.backend.backend_json import read_json,write_json_atomic
from app.config.config_paths import config_path,database_path
from app.config.config_app import SUPPORTED_GAMES
def load_settings():
 d=read_json(config_path(),{})
 games={}
 for g in SUPPORTED_GAMES:
  db=read_json(database_path(g),{})
  saved_game=d.get("games",{}).get(g,{})
  games[g]={"guid_start":saved_game.get("guid_start",""),"guid_end":saved_game.get("guid_end",""),"custom_regions":db.get("custom_regions",saved_game.get("custom_regions",[])),"default_export_path":saved_game.get("default_export_path","")}
 return {"selected_game":d.get("selected_game","Anno 117"),"worker_count":d.get("worker_count",4),"creator":d.get("creator",""),"creator_url":d.get("creator_url",""),"games":games}
def validate_guid_range(start,end):
 if not start or not end:raise ValueError("GUID Start and GUID End must be configured before importing maps.")
 if not start.isdigit() or not end.isdigit():raise ValueError("GUID values may contain digits only.")
 a,b=int(start),int(end)
 if a>b:raise ValueError("GUID Start must not be greater than GUID End.")
 return a,b
def save_settings(s):
 for g in SUPPORTED_GAMES:
  validate_guid_range(s["games"][g]["guid_start"],s["games"][g]["guid_end"])
  db=read_json(database_path(g),{})
  db["custom_regions"]=s["games"][g].get("custom_regions",[])
  write_json_atomic(database_path(g),db)
 config_payload={"selected_game":s.get("selected_game","Anno 117"),"worker_count":s.get("worker_count",4),"creator":s.get("creator",""),"creator_url":s.get("creator_url",""),"games":{g:{"guid_start":s["games"][g]["guid_start"],"guid_end":s["games"][g]["guid_end"],"default_export_path":s["games"][g].get("default_export_path","")} for g in SUPPORTED_GAMES}}
 write_json_atomic(config_path(),config_payload)

def get_custom_regions(settings, game):
 return list(settings.get("games",{}).get(game,{}).get("custom_regions",[]))


def save_custom_regions(game, regions):
 db=read_json(database_path(game),{})
 db["custom_regions"]=regions
 write_json_atomic(database_path(game),db)
