"""Build a versioned one-file executable with PyInstaller."""
from pathlib import Path
import shutil, subprocess, sys
ROOT=Path(__file__).resolve().parent

def main() -> int:
    """Validate source files, clean stale output, and invoke PyInstaller."""
    launcher=ROOT/"AnnoMapPackageCreator.py"; version=(ROOT/"version.txt").read_text(encoding="utf-8").strip()
    required=[launcher,ROOT/"anno_117.json",ROOT/"anno_1800.json",ROOT/"config.json"]
    missing=[str(p) for p in required if not p.exists()]
    if missing: raise FileNotFoundError("Missing build inputs: "+", ".join(missing))
    for folder in (ROOT/"build",ROOT/"dist"): shutil.rmtree(folder,ignore_errors=True)
    separator=";" if sys.platform.startswith("win") else ":"
    command=[sys.executable,"-m","PyInstaller","--noconfirm","--clean","--onefile","--windowed","--name",f"AnnoMapPackageCreator_v{version}"]
    for resource in ("version.txt","anno_117.json","anno_1800.json","config.json"):
        command += ["--add-data",f"{ROOT/resource}{separator}."]
    subprocess.run(command+[str(launcher)],cwd=ROOT,check=True)
    print(ROOT/"dist"/f"AnnoMapPackageCreator_v{version}{'.exe' if sys.platform.startswith('win') else ''}")
    return 0
if __name__=="__main__": raise SystemExit(main())
