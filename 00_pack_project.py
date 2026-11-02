"""Create a deterministic, reviewable source archive."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parent
EXCLUDED={".git",".venv","venv","build","dist","packed","__pycache__",".pytest_cache"}

def main() -> int:
    """Write selected project files to a versioned ZIP archive."""
    version=(ROOT/"version.txt").read_text(encoding="utf-8").strip(); out=ROOT/"packed"/f"AnnoMapPackageCreator_source_v{version}.zip"; out.parent.mkdir(exist_ok=True)
    files=[p for p in ROOT.rglob("*") if p.is_file() and not any(part in EXCLUDED for part in p.relative_to(ROOT).parts) and p.suffix not in {".pyc"}]
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files,key=lambda p:p.as_posix()): archive.write(path,path.relative_to(ROOT))
    print(f"{out} | {len(files)} files | {out.stat().st_size} bytes"); return 0
if __name__=="__main__": raise SystemExit(main())
