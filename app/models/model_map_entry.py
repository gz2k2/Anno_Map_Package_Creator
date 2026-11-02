from dataclasses import dataclass
@dataclass(slots=True)
class MapEntry:
 map_name:str;region:str;map_package:str;guid:int;map_type:str;map_file:str
 @classmethod
 def from_dict(cls,v):return cls(str(v.get("Map_Name","")),str(v.get("Region","")),str(v.get("Map_Package","")),int(v.get("GUID",0)),str(v.get("Type","Normal")),str(v.get("Map_File","")))
 def to_dict(self):return {"Map_Name":self.map_name,"Region":self.region,"Map_Package":self.map_package,"GUID":self.guid,"Type":self.map_type,"Map_File":self.map_file}
