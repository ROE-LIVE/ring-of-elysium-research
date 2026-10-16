"""Точечная высота исходного рельефа16010; PXBIN только читается, SDK не нужен.

Пока исследовательский инструмент: не учитывает здания/камни/мосты, не меняет
спавн или физику launcher. Поля/поза подтверждены Native019 PhysX3.3.4.
"""
import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import struct

SOURCE_SHA256 = frozenset((
    '4e28f2c6654fb8643821a612ce102719f3e70150f0f730d9a42bcb43d882097c',
    '8332fe282b7949acbe717b256638543c6aa32398744b84cfdfe25d7735467d6f',
))


def interpolate_height(samples, row_fraction, column_fraction):
    """Два диагональных разбиения PhysX3Common RVA18B80/18C41."""
    h00,h01,h10,h11 = (sample[0] for sample in samples)
    r,c = row_fraction,column_fraction
    if samples[0][1]&0x80:
        return (h00+c*(h01-h00)+r*(h11-h01) if c>r
                else h00+r*(h10-h00)+c*(h11-h10))
    return (h00+r*(h10-h00)+c*(h01-h00) if r+c<1
            else h11+(1-r)*(h01-h11)+(1-c)*(h10-h11))


def height_gradient(samples, row_fraction, column_fraction):
    """Производные выбранного треугольника по row/column."""
    h00,h01,h10,h11=(sample[0] for sample in samples)
    r,c=row_fraction,column_fraction
    if samples[0][1]&128:
        return (h11-h01,h01-h00) if c>r else (h10-h00,h11-h10)
    return (h10-h00,h01-h00) if r+c<1 else (h11-h01,h11-h10)


@dataclass(frozen=True)
class HeightField:
    path: Path
    rows: int = 2112
    columns: int = 2112
    samples_offset: int = 6464
    origin_x: float = 192000.0
    origin_y: float = 192000.0
    origin_z: float = 175002.671875
    spacing: float = 200.0
    height_scale: float = 5.340657711029053

    @classmethod
    def load(cls, path):
        path=Path(path)
        if path.stat().st_size != 17848756:
            raise ValueError('Нужен извлечённый IceLand2022 Linux/Win64 PXBIN17848756байт')
        with path.open('rb') as source:
            if hashlib.file_digest(source,'sha256').hexdigest() not in SOURCE_SHA256:
                raise ValueError('Неизвестный SHA исходного рельефа2022')
            source.seek(0);header=source.read(52)
            source.seek(1952+32);dimensions=source.read(8)
        if (header[:4]!=b'SEBD' or struct.unpack_from('<I',header,4)[0]!=0x3030400
                or struct.unpack_from('<I',header,32)[0]!=52
                or struct.unpack('<2I',dimensions)!=(2112,2112)):
            raise ValueError('Поля PXBIN не соответствуют подтверждённому heightfield')
        return cls(path)

    def height_at(self, x, y):
        if any(type(v) not in (int,float) or not math.isfinite(v) for v in (x,y)):
            raise ValueError('Нужны конечные world X/Y')
        # Actor quaternion(.5,.5,.5,.5): localX→worldY, localY→Z, localZ→X.
        row=(y-self.origin_y)/self.spacing
        column=(x-self.origin_x)/self.spacing
        if not (0<=row<self.rows-1 and 0<=column<self.columns-1):
            raise ValueError('Точка вне поддержанного внутреннего участка рельефа')
        r,c = math.floor(row),math.floor(column)
        samples=[]
        with self.path.open('rb') as source:
            for ri,ci in ((r,c),(r,c+1),(r+1,c),(r+1,c+1)):
                source.seek(self.samples_offset+(ri*self.columns+ci)*4)
                raw=source.read(4)
                if len(raw)!=4:
                    raise ValueError('Оборванные heightfield samples')
                samples.append(struct.unpack('<hBB',raw))
        height=interpolate_height(samples,row-r,column-c)
        pair=(samples[0][1]&127,samples[0][2]&127)
        dr,dc=height_gradient(samples,row-r,column-c)
        nx,ny=-dc*self.height_scale/self.spacing,-dr*self.height_scale/self.spacing
        norm=math.sqrt(nx*nx+ny*ny+1)
        normal=(nx/norm,ny/norm,1/norm)
        # В подтверждённом массиве все tessellation flags=0; оба native face совпали.
        triangle=None if samples[0][1]&128 else int(row-r+column-c>=1)
        face=None if triangle is None else 2*(r*self.columns+c)+triangle
        return dict(x=x,y=y,terrain_z=self.origin_z+self.height_scale*height,
                    row=r,column=c,row_fraction=row-r,column_fraction=column-c,
                    tessellation_flag=bool(samples[0][1]&128),material_pair=pair,
                    possible_hole=127 in pair,terrain_only=True,terrain_normal=normal,
                    face_index=face,material_index=None if triangle is None else pair[triangle])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--terrain-file',type=Path,required=True)
    parser.add_argument('--x',type=float,required=True)
    parser.add_argument('--y',type=float,required=True)
    args=parser.parse_args()
    try:result=HeightField.load(args.terrain_file).height_at(args.x,args.y)
    except (ValueError,OSError) as error:parser.error(str(error))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
