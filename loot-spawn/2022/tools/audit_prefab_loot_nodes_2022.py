"""Независимая сверка чужого списка XYZ с LayoutManager/prefab2022.

Проверяет геометрию и mSpawnerID, не доказывает RNG/плотность/привязку
контроллера к таблице предметов или доступность поверхности в игре.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def xml(path):
    if path.stat().st_size > 16*1024*1024:
        raise ValueError('XML больше16МиБ')
    data = path.read_bytes()
    text = re.sub(r'\s+\[[A-Za-z_]\w*\]="[^"]*"', '', data.decode('utf-8-sig'))
    # Редактор сохраняет буквальный '&' в описаниях; числовые поля не меняем.
    text = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)', '&amp;', text)
    return ET.fromstring(text), hashlib.sha256(data).hexdigest()


def xyz(element):
    values = tuple(float(element.attrib[k]) for k in 'xyz')
    if any(not math.isfinite(x) or abs(x)>10000000 for x in values):
        raise ValueError('Некорректная координата')
    return values


def world_point(instance, local):
    origin, scale = xyz(instance.find('mPosition')), xyz(instance.find('mScale'))
    matrix = [xyz(row) for row in instance.findall('mRotMatrix/m/m')]
    if len(matrix) != 3:
        raise ValueError('Матрица должна быть3x3')
    scaled = tuple(a*b for a,b in zip(local,scale))
    return tuple(round(base+math.fsum(a*b for a,b in zip(row,scaled))) for base,row in zip(origin,matrix))


def audit(extracted, candidates):
    data_root = Path(extracted)/'DATA'
    layout_path = data_root/'WORLD/EU_ICELAND_4096/CONFIG/LAYOUTMANAGER.XML'
    tree, layout_sha = xml(layout_path)
    instances = list(tree.iter('LayoutInstance'))
    candidates = Path(candidates)
    if candidates.stat().st_size > 16*1024*1024:
        raise ValueError('Список точек больше16МиБ')
    raw = candidates.read_bytes()
    rows = json.loads(raw)
    if not isinstance(rows,list) or not 1<=len(rows)<=100000:
        raise ValueError('Нужен список1..100000точек')
    cache, verified, mismatches, counters, seen = {}, [], [], Counter(), set()
    for row in rows:
        try:
            ordinal = row['Instance']
            if type(ordinal) is not int or not 0<=ordinal<len(instances):
                raise ValueError('Неверный номер LayoutInstance')
            instance = instances[ordinal]
            resource = instance.get('mParentName')
            if resource != row['Prefab'] or not re.fullmatch(r'Data\.layout\.prefab\.[A-Za-z0-9_.]+', resource, re.I):
                raise ValueError('Неверный prefab')
            key = (ordinal,row['Node'])
            if key in seen:
                raise ValueError('Повтор узла')
            seen.add(key)
            if resource not in cache:
                path = Path(extracted)/(resource.replace('.', '/')+'.XML').upper()
                prefab, sha = xml(path)
                nodes = {node.get('mName'):node for node in prefab.iter('mSpawnerNodes')}
                cache[resource] = (nodes, sha)
            node = cache[resource][0].get(row['Node'])
            if node is None:
                raise ValueError('В prefab нет узла')
            controller = int(node.get('mSpawnerID'))
            position = world_point(instance,xyz(node.find('mRelativePos')))
            if controller != row['Controller'] or position != (row['X'],row['Y'],row['Z']):
                raise ValueError('Controller/XYZ не совпали с источником')
            verified.append(dict(row,position_verified=True))
            counters[controller]+=1
        except (ValueError,KeyError,TypeError,AttributeError,OSError,ET.ParseError) as error:
            mismatches.append(dict(index=row.get('Index'),reason=str(error)))
    report = dict(map_id=16010,candidate_sha256=hashlib.sha256(raw).hexdigest(),
        layout_sha256=layout_sha,checked=len(rows),verified=len(verified),
        mismatches=mismatches[:30],mismatch_count=len(mismatches),
        prefabs={name:sha for name,(_,sha) in cache.items()},controllers=dict(counters),
        original_algorithm_verified=False,source_nodes=verified)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--extracted',type=Path,required=True)
    p.add_argument('--candidates',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=audit(a.extracted,a.candidates)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Проверено',result['checked'],'; совпало',result['verified'],'; расхождений',result['mismatch_count'])
