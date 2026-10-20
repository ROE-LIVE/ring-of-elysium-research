"""Собственный H1-каталог на проверенных исходных точках Iceland001 2022.

Тип точки -> группа LootControl и H1 с возвращением остаются гипотезами.
По умолчанию legacy-пул Citori/12ga/броня сохраняет прежние fixtures.
Опция peer-supported включает реализованные определения; веса перенормированы.
Исторический комментарий о гранатах устарел: актуальные границы в README пакета.
Подлинность исходных координат не означает подлинность выбранных предметов.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from export_loot_tables_2022 import export
from generate_loot_plan_2022 import generate
from loot_supported_definitions_2022 import PEER_SUPPORTED

POINTS_SHA = 'e6ee44da498bef4ee016b10222a75d094bf3d096ff80c1a6c6431dde4b4b5cf2'
XML_SHA = '2187235d2dfa8adaee356428725bcb8087c6dd03a38a2e5af4de8298a0107f3c'
SUPPORTED = (10402, 30004, 200102, 200103, 201002, 201003)


def build(points_path, tables_path, seed, excluded=(), scatter_cm=200, pool='legacy',
          authored_xyz=False, bounds_cm=None):
    path = Path(points_path)
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != POINTS_SHA:
        raise ValueError('Нужен проверенный экспорт Iceland001; SHA координат отличается')
    points = json.loads(raw)
    if points['map_id'] != 16010 or points['source_sha256'] != XML_SHA:
        raise ValueError('Неверная карта или источник точек')
    if type(scatter_cm) is not int or not 0 <= scatter_cm <= 200:
        raise ValueError('scatter_cm: 0..200')
    if type(authored_xyz) is not bool:
        raise ValueError('authored_xyz: нужен bool')
    if bounds_cm is not None:
        if (len(bounds_cm) != 4 or any(type(v) is not int for v in bounds_cm)
                or bounds_cm[0] >= bounds_cm[2] or bounds_cm[1] >= bounds_cm[3]):
            raise ValueError('bounds_cm: xmin ymin xmax ymax, целые и возрастающие')
        points['points'] = [p for p in points['points']
                            if bounds_cm[0] <= p['position_cm'][0] <= bounds_cm[2]
                            and bounds_cm[1] <= p['position_cm'][1] <= bounds_cm[3]]
        if not any(p['type_id'] in (1, 3, 5) and p['instance_id'] not in excluded
                   for p in points['points']):
            raise ValueError('В выбранном участке нет доступных точек 1/3/5')
    if authored_xyz:
        # На этажах/мебели случайный XY без collision query меняет поверхность.
        # Совпадающие модели допустимы; это наш диагностический режим, не RNG.
        scatter_cm = 0
    tables = export(tables_path, 16010)
    if pool not in ('legacy', 'peer-supported'):
        raise ValueError('Нужен явный pool legacy или peer-supported')
    # Расширение разрешает только уже реализованные ветки pickup. Полный
    # исходный pool и native модели всех типов этим не подтверждаются.
    supported = SUPPORTED if pool == 'legacy' else PEER_SUPPORTED
    entities, groups = [], []
    for cid in (1, 3, 5):
        selected = [r for r in points['points']
                    if r['type_id'] == cid and r['instance_id'] not in excluded]
        if not selected:
            groups.append(dict(control_id=cid, source_points=0,
                               generated_entities=0, occupied_points=0))
            continue
        controls = [r for r in tables['control']['rows'] if r['iID'] == str(cid)]
        if len(controls) != 1:
            raise ValueError('Нужна ровно одна группа LootControl')
        control = dict(controls[0], iRadius=str(scatter_cm))
        items = [r for r in tables['items']['rows'] if r['iCtrlID'] == str(cid)]
        plan = generate(control, items, [r['position_cm'] for r in selected],
                        seed * 16 + cid, 'H1', allowed=supported,
                        bundle_spacing_cm=0 if authored_xyz else 45)
        for row in plan['entities']:
            if row['item_id'] not in supported or not 1 <= row['quantity'] <= 100:
                raise ValueError('H1 выдала неподдержанный предмет или стопку')
            point = selected[row['point']]
            number = len(entities)
            entities.append(dict(index=100000 + number,
                entity_uid=0x00031d0003000000 + number, item_id=row['item_id'],
                quantity=row['quantity'], position=row['position'],
                source_point_id=point['instance_id'], source_type_id=cid,
                source_point_line=point['source_line'], source_item_row=row['source_row'],
                **({'source_direction': point['direction']} if authored_xyz else {})))
        groups.append(dict(control_id=cid, source_points=len(selected),
                           generated_entities=len(plan['entities']),
                           occupied_points=sum(n > 0 for n in plan['occupancy'])))
    result = dict(map_id=16010, radius_cm=2000, visible_limit=128, batch_limit=16,
                seed=seed, policy='H1', scatter_cm=scatter_cm,
                source_points_verified=True, original_algorithm_verified=False,
                original_aoi_verified=False, restricted_pool=list(supported),
                renormalized_weights=True,
                type_to_control_binding='Гипотеза: TypeId совпадает с iID LootControl',
                source_points_sha256=POINTS_SHA, source_xml_sha256=XML_SHA,
                sources={key: {k: tables[key][k] for k in ('path', 'sha256')}
                         for key in ('control', 'items')},
                excluded_point_ids=sorted(excluded), groups=groups, entities=entities)
    if pool != 'legacy':
        selected_rows = [r for r in tables['items']['rows'] if int(r['iCtrlID']) in (1,3,5)]
        selected_definitions = {int(r['iItemID']) for r in selected_rows}
        selected_definitions.update(int(value) for r in selected_rows for key,value in r.items()
                                    if key.startswith('iExtraItemID') and int(value)>0)
        missing = sorted(selected_definitions - set(supported))
        result.update(pool_profile=pool, full_original_pool=False,
                      native_catalog_types_verified=False,
                      selected_control_ids=[1,3,5],
                      selected_pool_definition_count=len(selected_definitions),
                      unsupported_selected_definitions=missing,
                      selected_pool_definitions_complete=not missing)
    if authored_xyz:
        result.update(authored_xyz=True, bundle_spacing_cm=0,
                      overlapping_models_possible=True,
                      original_orientation_verified=False,
                      source_direction_applied_to_wire=False)
    if bounds_cm is not None:
        result.update(bounds_cm=list(bounds_cm),
                      selection_policy='Замкнутый прямоугольник XY; наш тестовый участок')
    if not entities:
        raise ValueError('Получился пустой каталог: выберите другой seed или больший участок')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--points', type=Path, required=True)
    parser.add_argument('--tables', type=Path, default=Path('research/extracted/all-sfc/SFC/TableBin'))
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--scatter-cm', type=int, default=200)
    parser.add_argument('--authored-xyz', action='store_true',
                        help='Сохранять XYZ точки для основных/дополнительных предметов; модели могут совпадать')
    parser.add_argument('--pool', choices=('legacy', 'peer-supported'), default='legacy',
                        help='legacy сохраняет прежние fixtures; расширение требует native контроля')
    parser.add_argument('--exclude-point', type=int, nargs='*', default=[])
    parser.add_argument('--bounds-cm', type=int, nargs=4,
                        metavar=('XMIN', 'YMIN', 'XMAX', 'YMAX'),
                        help='Выбрать участок по авторским XY, не менять высоту/точки')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = build(args.points, args.tables, args.seed,
                   set(args.exclude_point), args.scatter_cm, args.pool, args.authored_xyz,
                   args.bounds_cm)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(json.dumps(dict(entities=len(result['entities']), groups=result['groups'],
                         item_counts=dict(Counter(r['item_id'] for r in result['entities'])),
                         output_sha256=hashlib.sha256(args.output.read_bytes()).hexdigest(),
                         original_algorithm_verified=False), ensure_ascii=False))


if __name__ == '__main__':
    main()
