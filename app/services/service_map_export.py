"""Game-neutral map-export dispatcher and validation entry point."""
from app.models.model_export import ExportRequest, ExportResult, LogCallback
from app.services.service_map_export_anno117 import export_anno117
from app.services.service_map_export_anno1800 import export_anno1800

_EXPORTERS = {
    "Anno 117": export_anno117,
    "Anno 1800": export_anno1800,
}


def export_map_package(request: ExportRequest, log: LogCallback) -> ExportResult:
    """Dispatch a validated export request to the selected game's exporter."""
    try:
        exporter = _EXPORTERS[request.game]
    except KeyError as error:
        raise ValueError(f"Unsupported game: {request.game}") from error
    return exporter(request, log)
