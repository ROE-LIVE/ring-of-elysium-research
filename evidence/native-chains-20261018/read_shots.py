"""Только известные49байт11DA/mode0 и события11DD одного выбранного опыта.

Не читает AUTH, ключи или остальные payload. Проекция не означает impact.
"""
from pathlib import Path
import json
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
RUN = ROOT / 'research/builds/2022/host-console-20261007/recovery-gun06-m4-edge-20261018-009'
CAP = RUN / 'game-endpoint'
rows = [json.loads(line) for line in (CAP / 'events.jsonl').read_text().splitlines()]
shots = []
for i, row in enumerate(rows):
    if row.get('kind') != 'application' or row.get('command') != '0x11da' or row['body_length'] != 49:
        continue
    previous = rows[i - 1]
    if previous.get('kind') != 'plaintext' or previous.get('length') != 83:
        continue
    path = CAP / previous['raw']
    if path.stat().st_size != 83:
        continue
    body = path.read_bytes()[34:]
    counter, mode = struct.unpack_from('>IB', body, 24)
    if mode != 0:
        continue
    values = struct.unpack_from('>6f', body)
    origin, endpoint = values[:3], values[3:]
    fraction = (371500 - origin[0]) / (endpoint[0] - origin[0])
    projected = [origin[j] + fraction * (endpoint[j] - origin[j]) for j in range(3)]
    shots.append(dict(counter=counter, timestamp=row['timestamp'], origin=origin,
                      aim=endpoint, projection_at_x371500=projected))
hits = [{k: v for k, v in row.items() if k not in ('remote', 'raw', 'hex')}
        for row in rows if row.get('kind') == 'actor_probe'
        and row.get('action') in ('hit_damage', 'hit_rejected')]
output = dict(scope='actual native requests; projection is not measured impact',
              shots=shots, hits=hits)
(HERE / 'native009-shots.json').write_text(json.dumps(output, indent=2) + '\n')
for row in shots[-4:]:
    print('shot', row['counter'], row['projection_at_x371500'])
for row in hits:
    print('hit', row.get('counter'), row.get('action'), row.get('hp'),
          row.get('collision_record_count'), row.get('penetration'), row.get('reason'))
