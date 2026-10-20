"""Высота и пересечение отрезка с исходным рельефом16010; SDK не нужен.

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

    def intersect_segment(self, origin, end):
        """Первое двустороннее пересечение с поверхностью, только terrain.

        Обход клеток по границам XY; это независимый геометрический контроль,
        не воспроизведение PhysX scene query/толщины/пробития. Концы должны
        находиться внутри подтверждённой области. Неизвестные holes и
        tessellation1 отвергаются, а не считаются свободной видимостью.
        """
        for point in (origin, end):
            if (not isinstance(point, (tuple, list)) or len(point) != 3
                    or any(type(v) not in (int, float) or not math.isfinite(v)
                           for v in point)):
                raise ValueError('Отрезок требует два конечных XYZ')
            if not (self.origin_x <= point[0] < self.origin_x+(self.columns-1)*self.spacing
                    and self.origin_y <= point[1] < self.origin_y+(self.rows-1)*self.spacing):
                raise ValueError('Конец отрезка вне внутренней области рельефа')
        direction=tuple(b-a for a,b in zip(origin,end))
        if not any(direction):
            raise ValueError('Нужен ненулевой отрезок')
        fractions={0.0,1.0}
        for axis,base in ((0,self.origin_x),(1,self.origin_y)):
            if direction[axis] == 0:
                continue
            lower,upper=sorted(((origin[axis]-base)/self.spacing,
                                (end[axis]-base)/self.spacing))
            for index in range(math.floor(lower)+1,math.ceil(upper)):
                fractions.add((base+index*self.spacing-origin[axis])/direction[axis])
        fractions=sorted(fractions)
        if len(fractions)>8192:
            raise ValueError('Слишком длинный обход рельефа')
        visited=0
        with self.path.open('rb') as source:
            for begin,finish in zip(fractions,fractions[1:]):
                middle=(begin+finish)/2
                column=math.floor((origin[0]+middle*direction[0]-self.origin_x)/self.spacing)
                row=math.floor((origin[1]+middle*direction[1]-self.origin_y)/self.spacing)
                samples=[]
                for ri,ci in ((row,column),(row,column+1),(row+1,column),(row+1,column+1)):
                    source.seek(self.samples_offset+(ri*self.columns+ci)*4)
                    raw=source.read(4)
                    if len(raw)!=4:raise ValueError('Оборванные heightfield samples')
                    samples.append(struct.unpack('<hBB',raw))
                if samples[0][1]&128 or 127 in (samples[0][1]&127,samples[0][2]&127):
                    raise ValueError('Неподдержанные tessellation1/hole127 в ray query')
                x=self.origin_x+column*self.spacing;y=self.origin_y+row*self.spacing
                visited+=1
                hits=[]
                for triangle_index in (0,1):
                    dr,dc=height_gradient(samples,triangle_index,triangle_index)
                    gy=dr*self.height_scale/self.spacing;gx=dc*self.height_scale/self.spacing
                    # Плоскость каждой грани привязана к её известной вершине.
                    anchor=samples[0][0] if triangle_index==0 else samples[3][0]
                    anchor_x=x+triangle_index*self.spacing;anchor_y=y+triangle_index*self.spacing
                    at_origin=(self.origin_z+self.height_scale*anchor
                               +gx*(origin[0]-anchor_x)+gy*(origin[1]-anchor_y))
                    denominator=direction[2]-gx*direction[0]-gy*direction[1]
                    if abs(denominator)<=1e-12*max(1,abs(direction[2]),abs(gx*direction[0]),abs(gy*direction[1])):
                        continue
                    fraction=(at_origin-origin[2])/denominator
                    if not begin-1e-9<=fraction<=finish+1e-9:continue
                    r=(origin[1]+fraction*direction[1]-y)/self.spacing
                    c=(origin[0]+fraction*direction[0]-x)/self.spacing
                    if (-1e-9<=r<=1+1e-9 and -1e-9<=c<=1+1e-9
                            and (r+c<=1+1e-9 if triangle_index==0 else r+c>=1-1e-9)):
                        hits.append((max(0,min(1,fraction)),triangle_index))
                if not hits:continue
                fraction,triangle_index=min(hits)
                point=tuple(a+fraction*d for a,d in zip(origin,direction))
                # На ребре height_at может выбрать соседнюю грань; нормаль и
                # material здесь берутся именно у пересечённого треугольника.
                dr,dc=height_gradient(samples,0 if triangle_index==0 else 1,
                                      0 if triangle_index==0 else 1)
                nx=-dc*self.height_scale/self.spacing;ny=-dr*self.height_scale/self.spacing
                norm=math.sqrt(nx*nx+ny*ny+1)
                return dict(fraction=fraction,position=point,
                            normal=(nx/norm,ny/norm,1/norm),row=row,column=column,
                            face_index=2*(row*self.columns+column)+triangle_index,
                            material_index=(samples[0][1]&127,samples[0][2]&127)[triangle_index],
                            visited_cells=visited,terrain_only=True)
        return None


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--terrain-file',type=Path,required=True)
    parser.add_argument('--x',type=float)
    parser.add_argument('--y',type=float)
    parser.add_argument('--origin',type=float,nargs=3,metavar=('X','Y','Z'))
    parser.add_argument('--end',type=float,nargs=3,metavar=('X','Y','Z'))
    args=parser.parse_args()
    ray=args.origin is not None or args.end is not None
    if ray:
        if args.origin is None or args.end is None or args.x is not None or args.y is not None:
            parser.error('Для отрезка нужны только --origin X Y Z и --end X Y Z')
    elif args.x is None or args.y is None:
        parser.error('Для точки нужны --x X --y Y')
    try:
        field=HeightField.load(args.terrain_file)
        result=(field.intersect_segment(args.origin,args.end) if ray else field.height_at(args.x,args.y))
    except (ValueError,OSError) as error:parser.error(str(error))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
