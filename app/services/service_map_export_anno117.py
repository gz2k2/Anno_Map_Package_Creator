"""Anno 117-specific assets.xml generation and export coordination."""
from pathlib import Path
import xml.etree.ElementTree as ET
from app.config.config_regions import get_fixed_regions
from app.models.model_export import ExportRequest, ExportResult, LogCallback
from app.services.service_map_export_common import copy_map_folders, finish_export, write_modinfo

def _region_map(request: ExportRequest) -> dict[str, str]:
    """Build the Anno 117 display-name to game-region-ID mapping."""
    result = {item['region']: str(item.get('id', '')).strip() for item in get_fixed_regions('Anno 117')}
    for item in request.settings.get('games', {}).get('Anno 117', {}).get('custom_regions', []):
        result[str(item.get('region', ''))] = str(item.get('id', '')).strip()
    return result

def island_placeholder_size(map_name: str) -> str:
    """Infer the Anno 117 placeholder size from the map name."""
    normalized = map_name.casefold().replace('-', '_').replace(' ', '_')
    if 'continental' in normalized or 'extralarge' in normalized or 'extra_large' in normalized:
        return 'XL'
    if 'large' in normalized:
        return 'Large'
    if 'medium' in normalized:
        return 'Medium'
    return ''

def write_assets_xml(request: ExportRequest) -> Path:
    """Write Anno 117 assets.xml to data/base/config/export/assets.xml."""
    assets_path = request.target / 'data' / 'base' / 'config' / 'export' / 'assets.xml'
    assets_path.parent.mkdir(parents=True, exist_ok=True)
    regions = _region_map(request)
    root = ET.Element('ModOps')
    mod_op = ET.SubElement(root, 'ModOp', {'GUID': '31778', 'Type': 'Append', 'Path': '/'})
    for entry in request.entries:
        map_file = Path(entry.map_file)
        mapped_region = regions.get(entry.region, '')
        if not mapped_region:
            raise ValueError(f'No Region ID mapping found for "{entry.region}" in Anno 117.')
        relative = f'data/{request.package_id}/{mapped_region.lower()}/islands/{map_file.parent.name}/{map_file.name}'
        mod_op.append(ET.Comment(f' {entry.map_name} '))
        asset = ET.SubElement(mod_op, 'Asset')
        ET.SubElement(asset, 'Template').text = 'RandomIsland'
        values = ET.SubElement(asset, 'Values')
        standard = ET.SubElement(values, 'Standard')
        ET.SubElement(standard, 'GUID').text = str(entry.guid)
        ET.SubElement(standard, 'Name').text = entry.map_name
        island = ET.SubElement(values, 'RandomIsland')
        ET.SubElement(island, 'FilePath').text = relative
        ET.SubElement(island, 'IslandRegion').text = mapped_region
        ET.SubElement(island, 'IslandDifficulty').text = 'Normal;Hard'
        if entry.map_type == 'Decoration':
            ET.SubElement(island, 'IslandType').text = 'Decoration'
        else:
            size = island_placeholder_size(entry.map_name)
            ET.SubElement(island, 'IslandType').text = 'Normal;Starter' if size in ('Large', 'XL') else 'Normal'
            if size:
                ET.SubElement(island, 'IslandPlaceholderSize').text = size
    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')
    tree.write(assets_path, encoding='utf-8', xml_declaration=False, short_empty_elements=False)
    return assets_path

def export_anno117(request: ExportRequest, log: LogCallback) -> ExportResult:
    """Run the complete Anno 117 export using shared copy and metadata services."""
    regions = _region_map(request)
    # Pass resolved game-facing IDs to the shared copy service so the physical
    # folder structure exactly matches the FilePath values written to assets.xml.
    request.package["_export_region_ids"] = regions
    copied = copy_map_folders(request, log)
    log(f'Created: {write_assets_xml(request)}')
    log(f'Created: {write_modinfo(request, anno_value=8)}')
    return finish_export(request, log, copied)
