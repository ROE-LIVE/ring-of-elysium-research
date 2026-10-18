"""Native: адресный административный урон, handoff, десять независимых смертей.

Это проверка управления состоянием/UID, не десять genuine gun kills и не AI.
"""
import json
from pathlib import Path
import sys
import time

ROOT = Path('/home/jovyan/imported/REsearch/ROE_SERVER')
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
from scene_action_2022 import enqueue

RUN = ROOT / 'research/builds/2022/host-console-20261007' / sys.argv[1]
QUEUE = RUN / 'live-commands.json'


def rows():
    return [json.loads(line) for line in (RUN / 'game-endpoint/events.jsonl').read_text().splitlines()]


def wait(predicate, after=0, seconds=15):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        found = [r for r in rows() if r['sequence'] > after and predicate(r)]
        if found:
            return found[-1]
        time.sleep(.1)
    raise RuntimeError('Нет ожидаемого события')


def damage(index, suffix):
    uid = hex(0x2040000800000 + index)
    label = f'roster005-{index}-{suffix}'
    mark = rows()[-1]['sequence']
    enqueue(QUEUE, dict(id=label, action='damage_npc', npc_uid=uid, damage=1000))
    result = wait(lambda r: r.get('kind') == 'live_state_action' and r.get('target') == uid, after=mark)
    if not result.get('accepted'):
        raise RuntimeError(str(result))
    print(label, result.get('hp'), flush=True)
    return result


first = damage(7, 'partial')
assert first['hp'] == 300
mark = rows()[-1]['sequence']
(RUN / 'udp-control.json').write_text(json.dumps(dict(id='roster005-target-cut',
    kind='drop_window', direction='client_to_server', seconds=20)) + '\n')
handoff = wait(lambda r: r.get('kind') == 'gameplay_handoff_complete', after=mark, seconds=85)
assert handoff['target_count'] == 10
states = {x['uid']: x for x in handoff['target_states']}
assert states['0x2040000800007']['hp'] == 300
assert all(x['hp'] == 1000 for uid, x in states.items() if uid != '0x2040000800007')
print('handoff preserved10targets and selectedHP300', flush=True)
assert damage(7, 'finish')['hp'] == 0
for index in range(10):
    if index == 7:
        continue
    assert damage(index, 'first')['hp'] == 300
    assert damage(index, 'second')['hp'] == 0

selected = [{k: v for k, v in r.items() if k not in ('remote', 'previous_remote', 'raw', 'hex')}
            for r in rows() if r.get('kind') in ('live_state_action', 'actor_probe',
                        'death_parcel_probe', 'gameplay_handoff_complete', 'match_statistics', 'match_result')]
(HERE / 'native005-roster-actions.json').write_text(json.dumps(selected, indent=2) + '\n')
actions = [r for r in selected if r.get('kind') == 'live_state_action' and r.get('accepted')]
assert len(actions) == 20
# Typed action возвращает сведения о transfer внутри live_state_action.corpse.
corpses = [r['corpse'] for r in selected if r.get('kind') == 'live_state_action'
           and (r.get('corpse') or {}).get('action') == 'death_inventory_transferred']
assert len(corpses) == 10 and len({r['owner'] for r in corpses}) == 10
print('10 native deaths/10unique death parcels; damage administrative, not gun hit statistics', flush=True)
