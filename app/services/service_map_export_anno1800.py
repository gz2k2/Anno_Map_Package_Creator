"""Anno 1800-specific assets.xml generation and export coordination."""
from pathlib import Path
import xml.etree.ElementTree as ET
from app.config.config_regions import get_fixed_regions
from app.models.model_export import ExportRequest, ExportResult, LogCallback
from app.services.service_map_export_common import copy_map_folders, finish_export, write_modinfo

def _region_map(request: ExportRequest) -> dict[str, str]:
    """Build the Anno 1800 display-name to game-region-ID mapping."""
    result = {item['region']: str(item.get('id', '')).strip() for item in get_fixed_regions('Anno 1800')}
    for item in request.settings.get('games', {}).get('Anno 1800', {}).get('custom_regions', []):
        result[str(item.get('region', ''))] = str(item.get('id', '')).strip()
    return result

def write_assets_xml(request: ExportRequest) -> Path:
    """Write Anno 1800 assets.xml to its game-specific export path."""
    assets_path = request.target / 'data' / 'config' / 'export' / 'main' / 'asset' / 'assets.xml'
    assets_path.parent.mkdir(parents=True, exist_ok=True)
    regions = _region_map(request)
    root = ET.Element('ModOps')
    root.append(ET.Comment(' START ADDING NEW ISLANDS TO ISLAND POOL '))
    mod_op = ET.SubElement(root, 'ModOp', {'GUID': '116676', 'Type': 'addNextSibling'})
    for entry in request.entries:
        map_file = Path(entry.map_file)
        mapped_region = regions.get(entry.region, '')
        if not mapped_region:
            raise ValueError(f'No Region ID mapping found for "{entry.region}" in Anno 1800.')
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
            ET.SubElement(island, 'IslandType').text = 'Normal;Starter' if entry.map_type == 'Starter' else 'Normal'
            ET.SubElement(island, 'IslandBaseName').text = entry.map_name
    root.append(ET.Comment(' END ADDING NEW ISLANDS TO ISLAND POOL '))
    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')
    tree.write(assets_path, encoding='utf-8', xml_declaration=False, short_empty_elements=False)
    return assets_path

def export_anno1800(request: ExportRequest, log: LogCallback) -> ExportResult:
    """Run the complete Anno 1800 export using shared copy and metadata services."""
    regions = _region_map(request)
    # Pass resolved game-facing IDs to the shared copy service so the physical
    # folder structure exactly matches the FilePath values written to assets.xml.
    request.package["_export_region_ids"] = regions
    copied = copy_map_folders(request, log)
    log(f'Created: {write_assets_xml(request)}')
    log(f'Created: {write_modinfo(request)}')
    return finish_export(request, log, copied)
