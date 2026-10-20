"""Учебный тир20: пять рядов по четыре уровня защиты на исходном рельефе."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from probe_iceland_heightfield_2022 import HeightField


def generate(heightfield, start=(365100,544000,259100), heading_degrees=330):
    angle=math.radians(heading_degrees)
    forward=(math.cos(angle),math.sin(angle));right=(forward[1],-forward[0])
    targets=[]
    for row in range(5):
        distance=1000*(row+1)
        for column in range(4):
            side=(column-1.5)*500+row*100
            x=round(start[0]+distance*forward[0]+side*right[0])
            y=round(start[1]+distance*forward[1]+side*right[1])
            terrain=heightfield.height_at(x,y)
            if terrain['possible_hole']:
                raise ValueError('Мишень попала в неизвестное отверстие рельефа')
            targets.append(dict(uid=hex(0x2040000900000+len(targets)+1),
                position=[x,y,round(terrain['terrain_z'])],armor_level=column,
                row=row+1,column=column+1,row_distance_m=distance//100,
                horizontal_distance_m=round(math.hypot(x-start[0],y-start[1])/100,3)))
    return dict(map_id=16010,start_position=list(start),layout='five-rows-four-levels-v1',
        first_row_cm=1000,row_spacing_cm=1000,column_spacing_cm=500,row_right_shift_cm=100,
        heading_degrees=heading_degrees,terrain_only=True,
        terrain_sha256=hashlib.sha256(heightfield.path.read_bytes()).hexdigest(),targets=targets)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--terrain',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();data=generate(HeightField.load(args.terrain))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Мишеней:',len(data['targets']))

if __name__=='__main__':main()
