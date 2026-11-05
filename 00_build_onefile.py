"""Build Anno Island Package Creator as a versioned one-file executable."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parent
APP_NAME = 'AnnoIslandPackageCreator'
LAUNCHER = ROOT / 'AnnoIslandPackageCreator.py'
PACKAGE_ROOT = ROOT / 'app'
REQUIREMENTS = ROOT / 'requirements.txt'
VERSION_FILE = ROOT / 'version.txt'
REQUIRED_MODULE_FILES = (PACKAGE_ROOT / 'main.py', PACKAGE_ROOT / 'config' / 'config_app.py', PACKAGE_ROOT / 'config' / 'config_paths.py', PACKAGE_ROOT / 'functions' / 'function_database.py', PACKAGE_ROOT / 'functions' / 'function_settings.py', PACKAGE_ROOT / 'functions' / 'function_update_check.py', PACKAGE_ROOT / 'services' / 'service_map_export.py', PACKAGE_ROOT / 'services' / 'service_map_export_anno117.py', PACKAGE_ROOT / 'services' / 'service_map_export_anno1800.py', PACKAGE_ROOT / 'services' / 'service_map_export_common.py', PACKAGE_ROOT / 'ui' / 'ui.py')

def _validate_sources() -> str:
    """Validate the current project layout and return the application version."""
    required = (LAUNCHER, PACKAGE_ROOT, REQUIREMENTS, VERSION_FILE, *REQUIRED_MODULE_FILES)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError('Missing build inputs: ' + ', '.join(missing))
    version = VERSION_FILE.read_text(encoding='utf-8').strip()
    if not version:
        raise ValueError('version.txt must contain a non-empty application version.')
    required_packages = ('customtkinter', 'packaging', 'PyInstaller')
    unavailable = [name for name in required_packages if importlib.util.find_spec(name) is None]
    if unavailable:
        raise RuntimeError('Missing Python build/runtime dependencies: ' + ', '.join(unavailable))
    return version

def _clean_output() -> None:
    """Remove stale PyInstaller output."""
    for folder in (ROOT / 'build', ROOT / 'dist'):
        shutil.rmtree(folder, ignore_errors=True)
    for spec_file in ROOT.glob('*.spec'):
        spec_file.unlink()

def _build_command(version: str) -> list[str]:
    """Create the PyInstaller command.

    version.txt is embedded in the one-file executable. JSON configuration and
    database files are deliberately not referenced by this build script.
    """
    separator = ';' if sys.platform.startswith('win') else ':'
    return [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onefile', '--windowed', '--name', f'{APP_NAME}_v{version}', '--add-data', f'{VERSION_FILE}{separator}.', '--exclude-module', 'pytest', '--exclude-module', 'tests', str(LAUNCHER)]

def main() -> int:
    """Validate, clean, build, and report the generated executable."""
    version = _validate_sources()
    _clean_output()
    subprocess.run(_build_command(version), cwd=ROOT, check=True)
    suffix = '.exe' if sys.platform.startswith('win') else ''
    artifact = ROOT / 'dist' / f'{APP_NAME}_v{version}{suffix}'
    if not artifact.is_file():
        raise FileNotFoundError(f'PyInstaller did not create the expected artifact: {artifact}')
    print(artifact)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
