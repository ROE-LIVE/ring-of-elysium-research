"""Только выбранные публичные ресурсы собственного клиента, без запуска игры."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from extract_prefab_loot_2022 import load_source,read_resource
from recover_winter_loot_presets_2022 import read_points

ROOT=Path(__file__).resolve().parents[1]
EXE_SHA='2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18'


def validate_destinations(client,cache,output):
    client,cache,output=map(lambda p:Path(p).resolve(),(client,cache,output))
    for target in (cache,output):
        if target==client or target.is_relative_to(client)or client.is_relative_to(target):
            raise ValueError('Кеш/выгрузка должны быть независимыми от клиента')
        if target.exists():raise ValueError('Нужен новый каталог кеша и новый каталог выгрузки')
    if cache==output or cache.is_relative_to(output)or output.is_relative_to(cache):
        raise ValueError('Кеш XML и публичная выгрузка должны быть разными деревьями')
    return client,cache,output


def export_source(client,cache,output):
    client,cache,output=validate_destinations(client,cache,output)
    with (client/'Europa_Client.exe').open('rb')as stream:
        if hashlib.file_digest(stream,'sha256').hexdigest()!=EXE_SHA:
            raise ValueError('Не тот корневой клиент2022; смещения другого EXE не применять')
    nodes,tables,summary=load_source(client,ROOT/'config/prefab-loot-sources.json',cache)
    record=json.loads((ROOT/'config/legacy-resource-source.json').read_text())
    legacy=read_resource(client,record)
    legacy_path=cache/'legacy-entitypoint.xml';legacy_path.write_bytes(legacy)
    points=read_points(legacy_path)['points']
    output.mkdir(parents=True,exist_ok=False)
    for filename,rows,fields in [('prefab-nodes.csv',nodes,['Index','Instance','Node','Prefab','Controller','X','Y','Z','position_verified']),
        ('legacy-entitypoints.csv',points,['instance_id','type_id','position_cm','direction','archetype','source_line'])]:
        with (output/filename).open('w',encoding='utf-8-sig',newline='')as stream:
            writer=csv.DictWriter(stream,fields,delimiter=';');writer.writeheader();writer.writerows(rows)
    manifest=json.loads((ROOT/'config/prefab-loot-sources.json').read_text())
    aliases={'control':'000001bb.xml','items':'00000a71.xml','vehicle_control':'0000083c.xml','vehicles':'000001a5.xml'}
    for kind,alias in aliases.items():
        tables[kind]['path']=next(r['path']for r in manifest['resources']if r.get('table_alias')==alias)
    (output/'loot-tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2)+'\n')
    summary.update(legacy_points=len(points),legacy_xml_sha256=hashlib.sha256(legacy).hexdigest(),
                   cache_resources_published=False,client_files_modified=False)
    (output/'source-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client',type=Path,required=True)
    parser.add_argument('--cache',type=Path,required=True,help='Новый каталог XML вне клиента/выгрузки, не добавлять в Git')
    parser.add_argument('--output',type=Path,required=True,help='Новый каталог только CSV/JSON')
    args=parser.parse_args()
    print(json.dumps(export_source(args.client,args.cache,args.output)))


if __name__=='__main__':main()
