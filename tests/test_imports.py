from app.models.model_map_entry import MapEntry
from app.functions.function_database import next_free_guid
from app.functions.function_settings import validate_guid_range
def test_next_guid_skips_used():assert next_free_guid([MapEntry("","","",10,"Normal","")],10,12)==11
def test_range():assert validate_guid_range("10","12")== (10,12)

def test_custom_regions_persist(monkeypatch, tmp_path):
 from app.functions import function_settings as fs
 db=tmp_path/"config_anno_117.json"
 db.write_text('{"schema_version": 1, "game": "Anno 117", "maps": []}',encoding="utf-8")
 monkeypatch.setattr(fs,"database_path",lambda game:db)
 fs.save_custom_regions("Anno 117",[{"region":"Test Region","id":"42"}])
 import json
 payload=json.loads(db.read_text(encoding="utf-8"))
 assert payload["custom_regions"]==[{"region":"Test Region","id":"42"}]

def test_package_id_sequence():
 from app.functions.function_database import _package_id_from_index,next_package_id
 assert _package_id_from_index(0)=="00"
 assert _package_id_from_index(1)=="01"
 assert _package_id_from_index(34)=="0y"
 assert _package_id_from_index(35)=="0z"
 assert _package_id_from_index(36)=="10"
 assert next_package_id([{"id":"00"},{"id":"01"}])=="02"


def test_map_type_defaults_to_normal():
 from app.models.model_map_entry import MapEntry
 entry=MapEntry.from_dict({"Map_Name":"A","GUID":1,"Map_File":"x.a7m"})
 assert entry.map_type=="Normal"
 assert entry.to_dict()["Type"]=="Normal"
