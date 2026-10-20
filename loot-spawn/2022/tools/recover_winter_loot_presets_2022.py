"""Карта авторских точек и аудит именованных таблиц лута Iceland 2022.

Экспортирует исходные параметры, не выдаёт iCount за доказанные вероятности
и совпадение TypeId/iID за установленную серверную привязку.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from export_loot_tables_2022 import read_table


def read_points(path):
    path = Path(path)
    if path.stat().st_size > 8 * 1024 * 1024:
        raise ValueError('XML точек превышает 8МиБ')
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    points = []
    for number, line in enumerate(text.splitlines(), 1):
        if 'InstanceID=' not in line:
            continue
        element = ET.fromstring(re.sub(r'\s+\[XlsProp\]="[^"]*"', '', line.strip()))
        row = element.attrib
        points.append(dict(instance_id=int(row['InstanceID']), type_id=int(row['TypeId']),
                           position_cm=[int(row[k]) for k in ('PosX', 'PosY', 'PosZ')],
                           direction=float(row['Direction']),
                           archetype=row.get('C_BaseInstanceName', ''), source_line=number))
    if not points or len({r['instance_id'] for r in points}) != len(points):
        raise ValueError('Нужны непустые точки с уникальными InstanceID')
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), points=points)


def audit(extracted):
    root = Path(extracted)
    base = root / 'DATA/SERVER/EU_ICELAND_4096'
    layouts = [read_points(base / 'ENTITYPOINTCONFIG.XML')]
    layouts.extend(read_points(base / f'ICELAND_00{i}/ENTITYPOINTCONFIG.XML')
                   for i in range(1, 5))
    table = root / 'DATA/TABLE/EULOOT'
    control = read_table(table / 'EUENTITYLOOTCONTROLCFGTABLE_1.XML', 16010)
    items = read_table(table / 'EUENTITYLOOTITEMCFGTABLE_1.XML', 16010)
    counts = Counter(r['type_id'] for r in layouts[1]['points'])
    presets = []
    for row in control['rows']:
        cid = int(row['iID'])
        pool = [r for r in items['rows'] if int(r['iCtrlID']) == cid]
        scalar = [int(v) for v in row['vNumPercent'].split(';')]
        presets.append(dict(control_id=cid, name=row['strName'],
                            radius=int(row['iRadius']), extra_max=int(row['iExtraMaxNum']),
                            scalar=scalar, array=row['num_percent_array'],
                            representations_agree=scalar == row['num_percent_array'],
                            same_number_point_count=counts[cid], pool_rows=len(pool),
                            sum_iCount=sum(int(r['iCount']) for r in pool),
                            source_line=row['source_line']))
    return dict(map_id=16010, original_algorithm_verified=False,
                type_to_control_verified=False, presets=presets,
                layouts=[dict(path=r['path'], sha256=r['sha256'],
                              point_count=len(r['points']),
                              type_counts=dict(Counter(p['type_id'] for p in r['points'])))
                         for r in layouts],
                variants_identical=len({r['sha256'] for r in layouts[1:]}) == 1,
                sources={k: {field: v[field] for field in ('path', 'sha256')}
                         for k, v in [('control', control), ('items', items)]}), layouts[1], items


def write_csv(path, rows):
    with Path(path).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter=';')
        writer.writeheader()
        writer.writerows(rows)


def write_map(path, points):
    # Встраиваются только числовые координаты; строки ресурсов не попадают в JS.
    data = [[p['instance_id'], p['type_id'], *p['position_cm'], p['source_line']]
            for p in points]
    html = '''<!doctype html><meta charset="utf-8"><title>Точки лута Iceland 2022</title>
<style>body{font:16px sans-serif;background:#18212b;color:#eee}canvas{background:#fff;max-width:95vw}
button{margin:4px}pre{white-space:pre-wrap}</style>
<h1>Авторские точки Iceland · 2022 · map16010</h1>
<p>Это схема XY, не изображение ландшафта. Содержимое точек не задано.
Цвета: 1 — синий, 3 — зелёный, 5 — красный. Остальные типы — серый.</p>
<label><input id="other" type="checkbox">Показать остальные типы</label>
<p>Колесо — масштаб; щелчок — ближайшая точка и её исходный XYZ/строка.
Масштабирование центрируется на указателе.</p>
<canvas id="map" width="1000" height="1000"></canvas><pre id="info"></pre>
<script>
const pts=__DATA__, c=document.getElementById('map'),ctx=c.getContext('2d');
let scale=1000/Math.max(Math.max(...pts.map(p=>p[2]))-Math.min(...pts.map(p=>p[2])),
Math.max(...pts.map(p=>p[3]))-Math.min(...pts.map(p=>p[3])))*.95;
let ox=Math.min(...pts.map(p=>p[2]))-25/scale,oy=Math.min(...pts.map(p=>p[3]))-25/scale;
function draw(){ctx.clearRect(0,0,1000,1000);for(const p of pts){
if(![1,3,5].includes(p[1])&&!document.getElementById('other').checked)continue;
ctx.fillStyle=({1:'#2255cc',3:'#168846',5:'#d04433'})[p[1]]||'#888';
ctx.fillRect((p[2]-ox)*scale,1000-(p[3]-oy)*scale,2,2);}}
function xy(e){const r=c.getBoundingClientRect();return[(e.clientX-r.left)*1000/r.width,
(e.clientY-r.top)*1000/r.height];}
c.addEventListener('wheel',e=>{e.preventDefault();const[x,y]=xy(e),a=ox+x/scale,b=oy+(1000-y)/scale;
scale*=e.deltaY<0?1.25:.8;ox=a-x/scale;oy=b-(1000-y)/scale;draw();},{passive:false});
c.onclick=e=>{const[x,y]=xy(e),a=ox+x/scale,b=oy+(1000-y)/scale;
const rows=pts.filter(p=>[1,3,5].includes(p[1])||document.getElementById('other').checked);
const p=rows.reduce((best,p)=>Math.hypot(p[2]-a,p[3]-b)<Math.hypot(best[2]-a,best[3]-b)?p:best);
document.getElementById('info').textContent=`InstanceID: ${p[0]}\\nTypeId: ${p[1]}\\nXYZ см: ${p.slice(2,5).join(', ')}\\nСтрока ENTITYPOINTCONFIG.XML: ${p[5]}\\nСвязь TypeId → LootControl остаётся гипотезой.`;};
document.getElementById('other').onchange=draw;draw();</script>'''
    Path(path).write_text(html.replace('__DATA__', json.dumps(data)), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extracted', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result, points, items = audit(args.extracted)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    write_csv(args.output / 'presets.csv', result['presets'])
    write_csv(args.output / 'points.csv', points['points'])
    # Поля дополнительных наборов различаются: сохраняем объединение колонок.
    fields = list(dict.fromkeys(key for row in items['rows'] for key in row))
    write_csv(args.output / 'items.csv', [{key: row.get(key, '') for key in fields}
                                        for row in items['rows']])
    write_map(args.output / 'map.html', points['points'])
    print(json.dumps(dict(point_count=len(points['points']), presets=len(result['presets']),
                          variants_identical=result['variants_identical']), ensure_ascii=False))


if __name__ == '__main__':
    main()
