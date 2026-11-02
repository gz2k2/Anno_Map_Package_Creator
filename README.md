# Anno Map Package Creator

English CustomTkinter desktop application for maintaining separate Anno 117 and Anno 1800 map-package databases.

## Features
- General tab with switchable database version and sortable columns: Map Name, Region, Map Package, GUID, Map File.
- Settings tab with digit-only GUID Start/End fields for both games and configurable worker count.
- Root-level `config.json` and two root-level JSON databases.
- GitHub, Ko-fi, background update check, one-file build, source pack, and GitHub release workflow.

## Run
```bash
python -m pip install -r requirements.txt
python AnnoMapPackageCreator.py
```

## Test and build
```bash
pytest
python 00_build_onefile.py
python 00_pack_project.py
```

## Configuration
`config.json`, `anno_117.json`, and `anno_1800.json` are writable root-level files. The dedicated repository URL in `app/config/config_app.py` must be updated after the new GitHub repository is created.

## Supported OS
Windows is the release target. Source execution is also possible on platforms supported by Python and CustomTkinter.

## License
No license has been selected yet.
