"""Два native Training: ID ручной команды одноразовый, NPC/HP создаются заново."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime

ROOT = Path('/home/jovyan/imported/REsearch/ROE_SERVER')
HERE = Path(__file__).resolve().parent
RUN = ROOT / 'research/builds/2022/host-console-20261007/recovery-gun05-repeat-20261018-006'
sys.path.insert(0, str(ROOT / 'tools'))
from scene_action_2022 import enqueue


def rows():
    path = RUN / 'game-endpoint/events.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def wait(test, after=0, seconds=240):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        found = [r for r in rows() if r['sequence'] > after and test(r)]
        if found:
            return found[-1]
        time.sleep(.25)
    raise RuntimeError('Не дождались события')


def ui(label, *action):
    subprocess.run([sys.executable, '-B', str(ROOT / 'research/builds/2022/iceland-gameplay-20261006/ui.py'),
                    'repeat006-' + label, *action], env=dict(os.environ, ROE_RUN_DIR=str(RUN)), check=True)


def damage(name):
    mark = rows()[-1]['sequence']
    enqueue(RUN / 'live-commands.json', dict(id=name, action='damage_npc',
            npc_uid='0x2040000800007', damage=1000))
    result = wait(lambda r: r.get('kind') == 'live_state_action' and r.get('id') == name,
                  after=mark, seconds=20)
    assert result.get('accepted') and result['hp'] == 300, result
    return result


# Продолжение006 после ручного исправления слишком частой F в первом helper.
first = next(r for r in rows() if r.get('kind') == 'winter_kit_initialized')
action = next(r for r in rows() if r.get('kind') == 'live_state_action' and r.get('accepted'))
finished = wait(lambda r: r.get('kind') == 'vehicle_probe' and r.get('action') == 'singleplayer_evacuation_finish')
remaining = 95 - (time.time() - datetime.fromisoformat(finished['timestamp']).timestamp())
if remaining > 0:
    time.sleep(remaining)
ui('newspaper')
ui('stats', '--click', '700', '964')
time.sleep(3)
ui('stats-open')
ui('return-lobby', '--click', '1300', '878')
time.sleep(18)
ui('lobby')
mark = rows()[-1]['sequence']
ui('training', '--click', '230', '360')
second = wait(lambda r: r.get('kind') == 'winter_kit_initialized', after=mark, seconds=240)
time.sleep(35)
events = rows()
created = [r for r in events if r['sequence'] > second['sequence'] and
           r.get('kind') == 'actor_probe' and r.get('action') == 'actor_created']
actions = [r for r in events if r.get('kind') == 'live_state_action']
assert len(actions) == 1, actions
ui('second-match')
mark = events[-1]['sequence']
(RUN / 'udp-control.json').write_text(json.dumps(dict(id='repeat006-new-match-cut',
    kind='drop_window', direction='client_to_server', seconds=20)) + '\n')
handoff = wait(lambda r: r.get('kind') == 'gameplay_handoff_complete', after=mark, seconds=90)
assert handoff['target_count'] == 10 and all(t['hp'] == 1000 for t in handoff['target_states']), handoff
enqueue(RUN / 'live-commands.json', dict(id='repeat006-new-id', action='damage_npc',
        npc_uid='0x2040000800007', damage=1000))
fresh = wait(lambda r: r.get('kind') == 'live_state_action' and r.get('accepted'),
             after=handoff['sequence'], seconds=20)
assert fresh['hp'] == 300, fresh
selected = [r for r in rows() if r.get('kind') in ('winter_kit_initialized', 'actor_probe',
    'live_state_action', 'gameplay_handoff_complete', 'match_statistics', 'match_finished')]
for row in selected:
    for key in ('remote', 'previous_remote', 'raw', 'hex'):
        row.pop(key, None)
(HERE / 'native006-repeat-match.json').write_text(json.dumps(dict(events=selected,
    first_action=action, second_handoff=handoff, fresh_action=fresh), indent=2) + '\n')
print('second match: ten fresh HP1000, old command not repeated; fresh ID accepted HP300', flush=True)
