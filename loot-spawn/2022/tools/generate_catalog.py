"""Offline H1 из опубликованных CSV/JSON; не запускает игру или сервер."""
import argparse
import csv
import json
from pathlib import Path
from generate_prefab_loot_catalog_2022 import build

ROOT=Path(__file__).resolve().parents[1]


def load_inputs(directory):
    directory=Path(directory)
    nodes=[]
    with (directory/'prefab-nodes.csv').open(encoding='utf-8-sig',newline='')as stream:
        for row in csv.DictReader(stream,delimiter=';'):
            if row['position_verified']!='True':raise ValueError('Несверенная точка')
            for key in ('Index','Instance','Controller','X','Y','Z'):row[key]=int(row[key])
            row['position_verified']=True;nodes.append(row)
    return nodes,json.loads((directory/'loot-tables.json').read_text(encoding='utf-8'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,default=ROOT/'data')
    parser.add_argument('--seed',type=int,required=True)
    parser.add_argument('--bounds-cm',nargs=4,type=int)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    nodes,tables=load_inputs(args.data)
    catalog=build(nodes,tables,args.seed,args.bounds_cm)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x',encoding='utf-8')as stream:
        json.dump(catalog,stream,ensure_ascii=False,separators=(',',':'));stream.write('\n')
    print(json.dumps(dict(seed=args.seed,points=catalog['source_point_count'],
                         entities=len(catalog['entities']),original_algorithm_verified=False)))


if __name__=='__main__':main()
