import json,os,tempfile
from pathlib import Path
def read_json(path,default):
 if not path.exists(): return default
 with path.open("r",encoding="utf-8") as f:return json.load(f)
def write_json_atomic(path,payload):
 fd,tmp=tempfile.mkstemp(prefix=path.name,suffix=".tmp",dir=path.parent)
 try:
  with os.fdopen(fd,"w",encoding="utf-8",newline="\n") as f:json.dump(payload,f,indent=2,ensure_ascii=False);f.write("\n")
  Path(tmp).replace(path)
 except Exception: Path(tmp).unlink(missing_ok=True);raise
