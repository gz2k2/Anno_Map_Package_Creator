from pathlib import Path
import zipfile
r=Path(__file__).parent;o=r/"AnnoMapPackageCreator_source.zip"
with zipfile.ZipFile(o,"w",zipfile.ZIP_DEFLATED) as z:
 for p in r.rglob("*"):
  if p.is_file() and "__pycache__" not in p.parts and p!=o:z.write(p,p.relative_to(r))
print(o)
