"""Публичные таблицы лута 2022 и явно приблизительная модель выбора.

Экспорт не утверждает, что bundled XML совпадает с действовавшим сервером.
Модель H1: массив задаёт проценты для 1..N предметов, остаток — пустая
точка; iCount используется как вес с возвращением. Нативный генератор
не подтверждён. Исходные точки зимней карты найдены отдельным SFC-проходом;
этот инструмент экспортирует таблицы и не связывает их с координатами.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import re
import xml.etree.ElementTree as ET


TABLES = {
    'control': '000001bb.xml', 'items': '00000a71.xml',
    'vehicle_control': '0000083c.xml', 'vehicles': '000001a5.xml',
}


def read_table(path, map_id):
    path = Path(path)
    if path.stat().st_size > 2*1024*1024:
        raise ValueError('Публичная XML-таблица превышает 2МиБ')
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    # Атрибут редактора с квадратными скобками не является валидным XML.
    root = ET.fromstring(re.sub(r'\s+\[XlsProp\]="[^"]*"', '', text))
    rows = []
    for element in root.iter():
        if element.get('iMapID') != str(map_id):
            continue
        row = dict(element.attrib)
        row['num_percent_array'] = [int(child.get('v'))
                                   for child in element.iter('vNumPercentArray')
                                   if child.get('v') is not None]
        row['source_line'] = next(number for number, line in enumerate(text.splitlines(), 1)
                                 if all(f'{key}="{value}"' in line
                                        for key, value in element.attrib.items()))
        rows.append(row)
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(),
                object=root.get('ObjName'), map_id=map_id, rows=rows)


def count_distribution(control, representation):
    """Только H1; неоднозначное представление обязан выбрать вызывающий."""
    if representation == 'array':
        percentages = control['num_percent_array']
    elif representation == 'scalar':
        percentages = [int(value) for value in control['vNumPercent'].split(';')]
    else:
        raise ValueError('Нужен явный выбор scalar или array')
    if not percentages or any(value < 0 for value in percentages) or sum(percentages) > 100:
        raise ValueError('H1 неприменима: неверная сумма процентов')
    return [100-sum(percentages), *percentages]


def weighted_index(weights, rng):
    if not weights or any(value < 0 for value in weights) or sum(weights) <= 0:
        raise ValueError('Нужны положительные суммарные веса')
    ticket = rng.randrange(sum(weights))
    for index, weight in enumerate(weights):
        if ticket < weight:
            return index
        ticket -= weight
    raise AssertionError('Не выбран вес')


def extra_bundle(row, rng):
    """H1 для явно названных iExtraItemWeight; не восстанавливает размещение."""
    options = [slot for slot in range(1, 8) if f'iExtraItemID{slot}' in row]
    if not options:
        return []
    weights = [int(row.get(f'iExtraItemWeight{slot}', '0')) for slot in options]
    if any(weight < 0 for weight in weights) or sum(weights) > 100:
        raise ValueError('H1 неприменима к дополнительным предметам')
    choice = weighted_index([100-sum(weights), *weights], rng)
    if choice == 0:
        return []
    slot = options[choice-1]
    count = int(row[f'iExtraItemCount{slot}'])
    quantity = int(row.get(f'iExtraItemStackCount{slot}', '1'))
    if not 1 <= count <= 7 or quantity < 1:
        raise ValueError('Неверное число дополнительных стопок')
    return [dict(item_id=int(row[f'iExtraItemID{slot}']), quantity=quantity)
            for _ in range(count)]


def simulate(control, items, points, seed, representation):
    if not 1 <= points <= 100000:
        raise ValueError('Число абстрактных точек: 1..100000')
    if not items:
        raise ValueError('Пустой пул; нельзя выдумывать связь с другой группой')
    rng = random.Random(seed)
    distribution = count_distribution(control, representation)
    weights = [int(row['iCount']) for row in items]
    occupancy, selected, extras = Counter(), Counter(), Counter()
    for _ in range(points):
        count = weighted_index(distribution, rng)
        occupancy[count] += 1
        for _ in range(count):
            row = items[weighted_index(weights, rng)]
            selected[row['iItemID']] += 1
            for extra in extra_bundle(row, rng):
                extras[str(extra['item_id'])] += extra['quantity']
    return dict(policy='H1: count percentages + weighted iCount with replacement',
                original_algorithm_verified=False, original_positions_available=False,
                representation=representation, seed=seed, abstract_points=points,
                count_weights=distribution, occupancy=dict(occupancy),
                selected_items=dict(selected), extra_units=dict(extras))


def export(tables, map_id):
    result = {key: read_table(Path(tables)/name, map_id) for key, name in TABLES.items()}
    pools = {}
    for row in result['items']['rows']:
        pools.setdefault(row['iCtrlID'], []).append(row)
    result['pool_summary'] = {key: dict(rows=len(rows), sum_iCount=sum(int(row['iCount']) for row in rows))
                              for key, rows in pools.items()}
    result['representation_conflicts'] = [dict(id=row['iID'], source_line=row['source_line'],
        scalar=row['vNumPercent'], array=row['num_percent_array'])
        for row in result['control']['rows']
        if [int(value) for value in row['vNumPercent'].split(';')] != row['num_percent_array']]
    result['missing_item_pools'] = [row['iID'] for row in result['control']['rows']
                                    if row['iID'] not in pools]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tables', type=Path, default=Path('research/extracted/all-sfc/SFC/TableBin'))
    parser.add_argument('--map', type=int, default=16010)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--sample-points', type=int)
    parser.add_argument('--ctrl', default='3')
    parser.add_argument('--seed', type=int, default=20261007)
    parser.add_argument('--representation', choices=('scalar', 'array'), default='array')
    args = parser.parse_args()
    result = export(args.tables, args.map)
    if args.sample_points is not None:
        controls = [row for row in result['control']['rows'] if row['iID'] == args.ctrl]
        if len(controls) != 1:
            parser.error('Нужна одна группа управления лутом')
        items = [row for row in result['items']['rows'] if row['iCtrlID'] == args.ctrl]
        result['simulation'] = simulate(controls[0], items, args.sample_points,
                                        args.seed, args.representation)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('Готово:', args.output)


if __name__ == '__main__':
    main()
