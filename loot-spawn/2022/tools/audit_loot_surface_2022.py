"""Сверяет выбранные точки лута16010 с исходным рельефом, не изменяя каталог.

Высота над terrain может означать этаж/мебель; это не ошибка сама по себе.
PXBIN и каталог читаются локально; геометрия зданий здесь не учитывается.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from probe_iceland_heightfield_2022 import HeightField


def audit(catalog_path, terrain_path):
    path = Path(catalog_path)
    if path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError('Каталог превышает16МиБ')
    raw = path.read_bytes()
    catalog = json.loads(raw.decode('utf-8-sig'))
    if catalog.get('map_id') != 16010:
        raise ValueError('Нужен каталог зимней карты16010')
    entities = catalog.get('entities')
    if not isinstance(entities, list) or not 1 <= len(entities) <= 50000:
        raise ValueError('Нужно1..50000 точек лута')
    terrain = HeightField.load(terrain_path)
    rows = []
    for item in entities:
        position = item['position']
        if (not isinstance(position, list) or len(position) != 3
                or any(type(v) is not int for v in position)):
            raise ValueError('Позиция должна содержать три целых сантиметра')
        sample = terrain.height_at(*position[:2])
        delta = position[2] - sample['terrain_z']
        status = ('possible_hole' if sample['possible_hole'] else
                  'below_terrain' if delta < -2 else
                  'above_terrain_or_static_surface' if delta > 20 else 'near_terrain')
        rows.append(dict(index=item['index'], item_id=item['item_id'],
                         x=position[0], y=position[1], z=position[2],
                         terrain_z_cm=round(sample['terrain_z'], 6),
                         delta_z_cm=round(delta, 6), terrain_face=sample['face_index'],
                         classification=status))
    return dict(map_id=16010, catalog_sha256=hashlib.sha256(raw).hexdigest(),
                terrain_only=True, buildings_and_props_checked=False, rows=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--terrain-file', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='Новый CSV; исходники не меняются')
    args = parser.parse_args()
    try:
        result = audit(args.catalog, args.terrain_file)
        # Не перезаписываем вход или уже существующий результат.
        with args.output.open('x', encoding='utf-8-sig', newline='') as target:
            writer = csv.DictWriter(target, fieldnames=list(result['rows'][0]), delimiter=';')
            writer.writeheader()
            writer.writerows(result['rows'])
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(json.dumps(dict(points=len(result['rows']), catalog_sha256=result['catalog_sha256'],
        below_terrain=sum(r['classification'] == 'below_terrain' for r in result['rows']),
        terrain_only=True, buildings_and_props_checked=False), ensure_ascii=False))


if __name__ == '__main__':
    main()
