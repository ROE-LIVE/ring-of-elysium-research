"""Один native501 в seeded исходной XY-точке; физика остаётся клиентской."""
from copy import deepcopy
import random
import struct

from airdrop_fixture_2022 import airdrop_notice


def randomize_airdrop(world, scene, index, seed, spawn_points):
    scene=deepcopy(scene)
    matches=[]
    for rule in scene:
        for response in rule['responses']:
            if int(response['command'],0)!=0x654b:continue
            if 'payload_file'in response:
                from pathlib import Path
                body=Path(response['payload_file']).read_bytes()
            else:body=bytes.fromhex(response['payload_hex'])
            if len(body)==117 and struct.unpack_from('>I',body,8)[0]==501:
                matches.append((rule,response,body))
    if len(matches)!=1:raise ValueError('Seeded native drop требует один117/501')
    rule,response,body=matches[0]
    at=rule['after_selection_delay_seconds']
    stage=max((s for s in world['stages']if s['at_seconds']<=at),key=lambda s:s['at_seconds'])
    safe=set(stage['previous_regions'])
    candidates=[p for p in spawn_points if index.region_id(p[2:])in safe and p[4]<301000]
    candidates=sorted(candidates,key=lambda p:tuple(p))
    if not candidates:raise ValueError('Нет исходной XY-точки в текущей безопасной области')
    point=random.Random(seed^0xa1d2022).choice(candidates)
    position=(point[2],point[3],301000)
    entity=bytearray(body);struct.pack_into('>3i',entity,20,*position)
    response.pop('payload_file',None);response['payload_hex']=entity.hex()
    notices=[r for r in rule['responses']if int(r['command'],0)==0x4a6]
    if len(notices)>1:raise ValueError('Повтор уведомления airdrop')
    if not notices:
        notices=[dict(command='0x4a6')];rule['responses'].extend(notices)
    notices[0].pop('payload_file',None);notices[0]['payload_hex']=airdrop_notice(position).hex()
    return scene,dict(airdrop_position_randomized=True,airdrop_uid=struct.unpack_from('>Q',body)[0],
        airdrop_start_position=list(position),airdrop_source_cell=list(point[:2]),
        airdrop_region=index.region_id(point[2:]),airdrop_candidates=len(candidates),
        airdrop_position_policy='source_spawn_xy_current_safe_client_fall',
        original_airdrop_algorithm_verified=False)
