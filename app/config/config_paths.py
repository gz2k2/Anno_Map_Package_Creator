from pathlib import Path
import sys
def root(): return Path(sys.executable).parent if getattr(sys,"frozen",False) else Path(__file__).resolve().parents[2]
def database_path(game): return root()/("config_anno_117.json" if game=="Anno 117" else "config_anno_1800.json")
def config_path(): return root()/"config.json"
def version_path(): return root()/"version.txt"
