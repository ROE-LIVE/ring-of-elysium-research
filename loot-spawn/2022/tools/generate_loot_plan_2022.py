"""Воспроизводимый локальный план лута; H1/H2 не выданы за исходный сервер.

H1 выбирает по iCount с возвращением. H2 расходует конечные квоты iCount.
Пространственные точки задаются явно. Исходный EntityPointConfig зимней
карты восстановлен отдельным SFC-проходом; произвольный ввод здесь не
получает автоматически статус проверенных исходных координат.
"""
import argparse
import json
import math
from pathlib import Path
import random
from export_loot_tables_2022 import export, count_distribution, weighted_index, extra_bundle


def generate(control, items, points, seed, policy, representation='array', allowed=None,
             bundle_spacing_cm=45):
    if policy not in ('H1', 'H2') or type(seed) is not int:
        raise ValueError('Нужны явные H1/H2 и целочисленный seed')
    if type(bundle_spacing_cm) is not int or not 0 <= bundle_spacing_cm <= 200:
        raise ValueError('bundle_spacing_cm: целое0..200')
    if not 1 <= len(points) <= 100000:
        raise ValueError('Нужно1..100000 явных точек')
    for p in points:
        if len(p) != 3 or any(type(x) is not int or abs(x) > 10000000 for x in p):
            raise ValueError('Точка должна содержать три ограниченных целых координаты')
    pool = [row for row in items if allowed is None or int(row['iItemID']) in allowed]
    if not pool:
        raise ValueError('Пустой пул')
    weights = [int(row['iCount']) for row in pool]
    if any(x < 0 for x in weights) or sum(weights) == 0:
        raise ValueError('Неверные веса/квоты')
    initial = weights[:]
    rng = random.Random(seed)
    distribution = count_distribution(control, representation)
    radius = int(control.get('iRadius', '200'))
    if not 0 <= radius <= 10000:
        raise ValueError('Радиус вне диапазона')
    entities, occupancy = [], []
    for point_index, point in enumerate(points):
        count = weighted_index(distribution, rng)
        if policy == 'H2' and count > sum(weights):
            raise ValueError('Квоты H2 исчерпаны; автоматического пополнения нет')
        occupancy.append(count)
        for _ in range(count):
            selected = weighted_index(weights, rng)
            row = pool[selected]
            if policy == 'H2':
                weights[selected] -= 1
            # Собственная локальная раскладка в круге; Z задаёт автор точек.
            angle, distance = rng.uniform(0, 2*math.pi), radius*math.sqrt(rng.random())
            pos = (point[0]+round(math.cos(angle)*distance),
                   point[1]+round(math.sin(angle)*distance), point[2])
            quantity = int(row.get('iStackCount', '1'))
            if not 1 <= quantity <= 999:
                raise ValueError('Неверный размер исходной стопки iStackCount')
            bundle = [dict(item_id=int(row['iItemID']), quantity=quantity), *extra_bundle(row, rng)]
            for n, item in enumerate(bundle):
                entities.append(dict(point=point_index, source_row=row['iID'],
                    position=[pos[0]+n*bundle_spacing_cm, pos[1], pos[2]], **item))
    return dict(map_id=int(control['iMapID']), control_id=control['iID'],
                policy=policy, seed=seed, representation=representation,
                original_algorithm_verified=False, original_positions_available=False,
                restricted_pool=allowed is not None, renormalized_weights=allowed is not None,
                input_points=points, occupancy=occupancy, entities=entities,
                initial_quotas=initial if policy == 'H2' else None,
                remaining_quotas=weights if policy == 'H2' else None)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tables', type=Path, default=Path('research/extracted/all-sfc/SFC/TableBin'))
    p.add_argument('--points', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--seed', type=int, required=True)
    p.add_argument('--policy', choices=('H1', 'H2'), required=True)
    p.add_argument('--map', type=int, default=16010)
    p.add_argument('--control', default='3')
    p.add_argument('--representation', choices=('array', 'scalar'), default='array')
    p.add_argument('--allowed-items', type=int, nargs='+', help='Явно ограничить пул; веса будут перенормированы')
    a = p.parse_args()
    tables = export(a.tables, a.map)
    controls = [x for x in tables['control']['rows'] if x['iID'] == a.control]
    if len(controls) != 1:
        p.error('Группа управления должна существовать ровно один раз')
    items = [x for x in tables['items']['rows'] if x['iCtrlID'] == a.control]
    plan = generate(controls[0], items, json.loads(a.points.read_text()), a.seed,
                    a.policy, a.representation, a.allowed_items)
    plan['sources'] = {key: {k: tables[key][k] for k in ('path','sha256')}
                       for key in ('control','items')}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n')
    print('План:', len(plan['entities']), 'предметов;', a.policy)


if __name__ == '__main__':
    main()
