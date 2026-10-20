"""Seeded H1 на сверенных prefab-узлах Iceland2022, без перемещения XYZ.

Состав/веса/стопки из исходных таблиц; контроллер→пул и H1 с возвращением
остаются локальной политикой. Не гарантируем предмет в каждом здании.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from export_loot_tables_2022 import export
from generate_loot_plan_2022 import generate
from generate_winter_loot_catalog_2022 import PEER_SUPPORTED


def build(nodes, tables, seed, bounds=None):
    if type(seed) is not int or not -(2**63)<=seed<2**63:
        raise ValueError('Seed — знаковое64бит целое')
    if bounds is not None and (len(bounds)!=4 or any(type(v) is not int for v in bounds)
            or bounds[0]>=bounds[2] or bounds[1]>=bounds[3]):
        raise ValueError('Границы xmin/ymin/xmax/ymax')
    selected=[];seen=set()
    for row in nodes:
        key=row['Index'];point=[row[k] for k in ('X','Y','Z')]
        if (type(key) is not int or key in seen or row.get('position_verified') is not True
                or row['Controller'] not in (1,3,5)
                or any(type(x) is not int or abs(x)>10000000 for x in point)):
            raise ValueError('Нужны уникальные сверенные XYZ/контроллеры1/3/5')
        seen.add(key)
        if bounds is None or bounds[0]<=point[0]<=bounds[2] and bounds[1]<=point[1]<=bounds[3]:
            selected.append(row)
    entities=[]
    for controller in (1,3,5):
        group=sorted((r for r in selected if r['Controller']==controller),key=lambda r:r['Index'])
        if not group:continue
        controls=[r for r in tables['control']['rows'] if int(r['iID'])==controller]
        if len(controls)!=1:raise ValueError('Нужна одна строка исходного LootControl')
        control=dict(controls[0],iRadius='0')
        pool=[r for r in tables['items']['rows'] if int(r['iCtrlID'])==controller]
        plan=generate(control,pool,[[r[k] for k in ('X','Y','Z')] for r in group],
                      seed*16+controller,'H1',allowed=PEER_SUPPORTED,bundle_spacing_cm=0)
        for item in plan['entities']:
            if item['item_id'] not in PEER_SUPPORTED or not 1<=item['quantity']<=100:
                raise ValueError('Результат не поддержан текущим pickup')
            source=group[item['point']];number=len(entities)
            entities.append(dict(index=2000000+number,entity_uid=0x31d0900000000+number,
                item_id=item['item_id'],quantity=item['quantity'],position=item['position'],
                source_point_id=source['Index'],source_instance=source['Instance'],
                source_node=source['Node'],source_prefab=source['Prefab'],source_item_row=item['source_row']))
    if not 1<=len(entities)<=50000:
        raise ValueError('H1 должен дать1..50000предметов; выберите другой seed/участок')
    return dict(map_id=16010,radius_cm=2000,visible_limit=128,batch_limit=16,
                seed=seed,policy='prefab-H1-v1',original_algorithm_verified=False,
                source_points_verified=True,controller_binding_verified=False,
                renormalized_weights=True,source_point_count=len(selected),entities=entities)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audit',type=Path,required=True)
    p.add_argument('--tables',type=Path,default=Path('research/extracted/all-sfc/SFC/TableBin'))
    p.add_argument('--seed',type=int,required=True)
    p.add_argument('--bounds-cm',nargs=4,type=int)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.audit.stat().st_size>16*1024*1024:p.error('Аудит превышает16МиБ')
    raw=a.audit.read_bytes();audit=json.loads(raw)
    if (audit.get('map_id')!=16010 or audit.get('mismatch_count')!=0
            or audit.get('checked')!=audit.get('verified')
            or audit.get('verified')!=len(audit.get('source_nodes',[]))):
        p.error('Нужен завершённый аудит исходных узлов без расхождений')
    result=build(audit['source_nodes'],export(a.tables,16010),a.seed,a.bounds_cm)
    result.update(audit_sha256=hashlib.sha256(raw).hexdigest(),layout_sha256=audit['layout_sha256'])
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(dict(seed=a.seed,points=result['source_point_count'],entities=len(result['entities']),
                         item_counts=dict(Counter(r['item_id'] for r in result['entities'])))))
