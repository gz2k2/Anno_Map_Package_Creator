"""Game-neutral map-export dispatcher and validation entry point."""
from pathlib import Path
import shutil
from app.models.model_export import ExportRequest, ExportResult, LogCallback
from app.services.service_map_export_anno117 import export_anno117
from app.services.service_map_export_anno1800 import export_anno1800
_EXPORTERS = {'Anno 117': export_anno117, 'Anno 1800': export_anno1800}

def export_map_package(request: ExportRequest, log: LogCallback) -> ExportResult:
    """Dispatch a validated export request to the selected game's exporter."""
    try:
        exporter = _EXPORTERS[request.game]
    except KeyError as error:
        raise ValueError(f'Unsupported game: {request.game}') from error
    result = exporter(request, log)
    for folder_value in request.package.get('additional_files', []):
        source = Path(folder_value)
        if not source.is_dir():
            raise ValueError(f'Additional Files folder does not exist: {source}')
        target = request.target
        for source_item in source.iterdir():
            target_item = target / source_item.name
            if source_item.is_dir():
                shutil.copytree(source_item, target_item, dirs_exist_ok=True)
            else:
                target_item.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_item, target_item)
        for copied_file in source.rglob('*'):
            if copied_file.is_file():
                log(f'Copied additional file: {target / copied_file.relative_to(source)}')
    return result
