"""Выдать карточку CSV без игры, сервисов и сторонних зависимостей."""
import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'docs/recovery/mechanics-2022.csv'
GATES = dict(contract=10, wire=15, data=15, server=20, client=20, scenario=20)


def load_plan(path=PLAN):
    with Path(path).open(encoding='utf-8-sig', newline='') as source:
        rows = list(csv.DictReader(source, delimiter=';'))
    ids, numbers = set(), set()
    if not rows:
        raise ValueError('Пустой план')
    for row in rows:
        if None in row or any(v is None for v in row.values()):
            raise ValueError('Неполная CSV-строка')
        ident, number = row['id'], int(row['sequence'])
        if not ident or ident in ids or number in numbers or number < 1:
            raise ValueError('Повторный/пустой ID или sequence')
        ids.add(ident)
        numbers.add(number)
        if any(row[k] not in ('0', '1', '2') for k in GATES):
            raise ValueError(f'{ident}: этапы0/1/2')
        pct = sum(int(row[k])*weight/2 for k, weight in GATES.items())
        if float(row['progress_pct']) != pct:
            raise ValueError(f'{ident}: неверный процент этапов')
    if numbers != set(range(1, len(rows)+1)):
        raise ValueError('Пропуск sequence')
    if any(v not in ids for row in rows for v in row['depends_on'].split('|') if v):
        raise ValueError('Неизвестная зависимость')
    return sorted(rows, key=lambda r: int(r['sequence']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choices = parser.add_mutually_exclusive_group(required=True)
    choices.add_argument('--task', help='Стабильный ID или sequence')
    choices.add_argument('--list', action='store_true')
    choices.add_argument('--next', action='store_true')
    choices.add_argument('--validate', action='store_true')
    args = parser.parse_args()
    rows = load_plan()
    if args.validate:
        print(f'OK: {len(rows)} задач; ID/sequence/этапы/зависимости. Внешние доказательства не проверены.')
        return
    if args.list:
        for row in rows:
            print(f"{row['sequence']:>3} {row['id']:<8} {row['work_state']:<18} {row['mechanic']}")
        return
    selected = [r for r in rows if (r['work_state'] == 'ready' if args.next else args.task in (r['id'], r['sequence']))]
    if not selected:
        if args.next:
            print('Нет ready-задачи. Заблокированные пункты требуют отдельного разбора; см. STATUS.md.')
            return
        parser.error('Задача не найдена')
    row = selected[0]
    print('Исторические paths/commands относятся к исходному ROE_SERVER. Ничего не запускается.\n')
    for key in ('sequence', 'id', 'build', 'work_state', 'mechanic', 'progress_pct',
                'agent_goal', 'acceptance', 'next_step', 'limitations', 'depends_on',
                'signals', 'sources', 'evidence', 'primary_ref', 'edit_targets', 'verify_command'):
        print(f'{key}: {row[key]}')


if __name__ == '__main__':
    main()
