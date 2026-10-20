"""Реестр зимнего pool2022 и границ peer; не реконструкция исходного RNG.

Группы1/3/5 выбраны явно. Связь TypeId точки с CtrlID остаётся гипотезой.
Имена/слоты берутся из публичных определений; наличие определения не
означает подтверждение модели на земле или успешного native pickup.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'server/directory'))
from export_loot_tables_2022 import export
from weapon_probe_2022 import (
    AMMUNITION_WEIGHTS, EQUIPMENT_SLOTS, GUN_PROFILES, MEDICAL_PROFILES,
    SUPPORTED_ATTACHMENTS)
from throwable_inventory_2022 import THROWABLE_PROFILES


def definitions(path):
    path = Path(path)
    raw = path.read_bytes()
    if len(raw) > 2 * 1024 * 1024:
        raise ValueError('Таблица определений превышает 2МиБ')
    text = raw.decode('utf-8-sig')
    normalized = re.sub(r'\s+\[XlsProp\]="[^"]*"', '', text)
    # A81 содержит соседние атрибуты без пробела; исправляем только разделитель
    # в памяти. Исходные байты, SHA и номера строк сохраняются.
    normalized, separators = re.subn(r'(?<=")(?=[A-Za-z_]\w*=")', ' ', normalized)
    root = ET.fromstring(normalized)
    rows = {}
    line_by_id = {}
    for line, value in enumerate(text.splitlines(), 1):
        match = re.search(r'\bdwStringID="(\d+)"', value)
        if match:
            line_by_id.setdefault(int(match.group(1)), []).append(line)
    for element in root.iter():
        value = element.get('dwStringID')
        if value is None or not value.isdecimal():
            continue
        definition = int(value)
        rows.setdefault(definition, []).append(dict(
            attributes=dict(element.attrib), source_lines=line_by_id[definition]))
    return rows, dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(),
                      object=root.get('ObjName'), adjacent_attribute_separators=separators)


def audit(tables, controls=(1, 3, 5)):
    tables = Path(tables)
    exported = export(tables, 16010)
    selected = [r for r in exported['items']['rows'] if int(r['iCtrlID']) in controls]
    if not selected:
        raise ValueError('Нет записей выбранных групп')
    catalog, sources = {}, {}
    for name, file in [('equipment', '00000a89.xml'), ('items', '00000a81.xml')]:
        rows, sources[name] = definitions(tables / file)
        for definition, entries in rows.items():
            catalog.setdefault(definition, []).extend(dict(x, source=name) for x in entries)
    primary = {int(r['iItemID']) for r in selected}
    extras = {int(value) for r in selected for key, value in r.items()
              if key.startswith('iExtraItemID') and int(value) > 0}
    support = [('gun', GUN_PROFILES), ('ammunition', AMMUNITION_WEIGHTS),
               ('equipment', EQUIPMENT_SLOTS), ('medical', MEDICAL_PROFILES),
               ('attachment', SUPPORTED_ATTACHMENTS), ('throwable_inventory', THROWABLE_PROFILES)]
    result = []
    for definition in sorted(primary | extras):
        entries = catalog.get(definition, [])
        kind = next((name for name, ids in support if definition in ids), 'unsupported')
        attrs = entries[0]['attributes'] if len(entries) == 1 else {}
        uses = [dict(control_id=int(r['iCtrlID']), source_row=r['iID'],
                     source_line=r['source_line'], count=r['iCount'],
                     stack_count=r.get('iStackCount', '1'))
                for r in selected if int(r['iItemID']) == definition]
        result.append(dict(item_id=definition, primary=definition in primary,
            extra=definition in extras, name=attrs.get('szSimplifiedName', attrs.get('dwStringIDName', '')),
            category=attrs.get('mCategory', ''), subcategory=attrs.get('mSubCategory', ''),
            positions=attrs.get('szPosition', ''), pack_max=attrs.get('nPackMax', ''),
            weight=attrs.get('nWeight', ''), peer_kind=kind,
            peer_supported=kind != 'unsupported',
            native_catalog_verified=False, definition_matches=len(entries),
            definition_sources=[dict(source=x['source'], lines=x['source_lines']) for x in entries],
            pool_uses=uses))
    return dict(build='2022-0.2.989.0-x64', map_id=16010, controls=list(controls),
        type_to_control_verified=False, original_algorithm_verified=False,
        selected_pool_rows=len(selected), primary_definitions=len(primary),
        extra_definitions=len(extras), unique_definitions=len(primary | extras),
        supported_definitions=sum(r['peer_supported'] for r in result),
        missing_definitions=[r['item_id'] for r in result if not r['peer_supported']],
        ambiguous_or_missing_definitions=[r['item_id'] for r in result if r['definition_matches'] != 1],
        sources=dict(sources, pool={k: exported['items'][k] for k in ('path', 'sha256')}),
        entities=result)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tables', type=Path, default=Path('research/extracted/all-sfc/SFC/TableBin'))
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    value = audit(a.tables)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    fields = ('item_id', 'name', 'primary', 'extra', 'peer_kind', 'peer_supported',
              'native_catalog_verified', 'category', 'positions', 'pack_max', 'weight', 'definition_matches')
    with a.output.with_suffix('.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=';', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(value['entities'])
    print(json.dumps({key: value[key] for key in ('selected_pool_rows', 'unique_definitions',
         'supported_definitions', 'ambiguous_or_missing_definitions')}))


if __name__ == '__main__':
    main()
