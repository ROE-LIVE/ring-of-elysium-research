"""Ограниченный контроль entry/exit по sourcemesh против двух живых hit; без изменения peer."""
from pathlib import Path
import json,math,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
sys.path.insert(0,str(ROOT/'server/directory'))
from collision_mesh_2022 import load_collision_meshes
from collision_triangle_2022 import segment_triangle_entry
mesh=load_collision_meshes(HERE/'rock-mesh-manifest.json')[0]
cases=[('native014',json.loads((HERE/'offline-primary144-replay.json').read_text())['event'])]
seventeen=json.loads((HERE/'native017-extended-hit-validation.json').read_text())
cases.append(('native017',next(e for e in seventeen['events'] if e.get('collision_record_count')==2)))
rows=[]
for name,e in cases:
 origin,end=e['gun_origin'],e['hit_impact'];delta=tuple(b-a for a,b in zip(origin,end))
 intersections=[]
 for face,tri in enumerate(mesh.triangles):
  fraction=segment_triangle_entry(origin,end,tri)
  if fraction is not None:intersections.append((fraction,face))
 intersections.sort();points=[]
 for fraction,face in intersections:
  point=tuple(a+fraction*d for a,d in zip(origin,delta))
  if points and math.dist(points[-1]['point'],point)<.001:continue
  points.append(dict(point=point,face=face,fraction=fraction))
 records=e['collision_records'];entry,exit=[r['point'] for r in records]
 row=dict(run=name,source_intersections=points,native_record_thickness_cm=math.dist(entry,exit),
          native_entry=entry,native_exit=exit)
 if len(points)==2:
  entry2,exit2=[p['point'] for p in points]
  row.update(source_ray_thickness_cm=math.dist(entry2,exit2),entry_error_cm=math.dist(entry,entry2),exit_error_cm=math.dist(exit,exit2))
  def next_energy(t):return 47-(47*.16+(1/.45)*3*(3/2.5*1.25)+t*t/(.45*154.83839416503906))
  row.update(energy_from_native_records=next_energy(math.dist(entry,exit)),energy_from_source_ray=next_energy(math.dist(entry2,exit2)))
 rows.append(row)
result=dict(scope='OFFLINE source ray vs genuine native records; no authoritative damage or implemented penetration',rows=rows)
(HERE/'through-ray-source-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
