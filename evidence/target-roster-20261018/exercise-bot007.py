"""Native singleton BOT05: лут→safe→C2S20s→текущий death inventory."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('/home/jovyan/imported/REsearch/ROE_SERVER')
HERE = Path(__file__).resolve().parent
RUN = ROOT / 'research/builds/2022/host-console-20261007/recovery-bot05-handoff-20261018-007'
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
        time.sleep(.2)
    raise RuntimeError('Не дождались события')


def sample(label, uid):
    candidates = []
    for proc in Path('/proc').iterdir():
        if not proc.name.isdecimal():
            continue
        try:
            cmd = (proc / 'cmdline').read_bytes().split(b'\0')
            if cmd[0] == b'./Europa_Client.exe' and (proc / 'cwd').resolve() == ROOT / 'runtime/client':
                candidates.append(int(proc.name))
        except (OSError, PermissionError):
            pass
    assert len(candidates) == 1, candidates
    (RUN / 'game-pid.txt').write_text(str(candidates[0]))
    tool = ROOT / 'research/builds/2022/recovery/095-bot01/20261012T0450-active-lifecycle/sample_target.py'
    path = HERE / ('native007-' + label + '.json')
    subprocess.run(['sudo', '-n', sys.executable, '-B', str(tool), str(RUN), uid, str(path)], check=True)
    values = json.loads(path.read_text())
    assert values.get('actor_present') and 'error' not in values, values
    return values


wait(lambda r: r.get('kind') == 'winter_kit_initialized', seconds=300)
safe = wait(lambda r: r.get('kind') == 'actor_probe' and r.get('action') == 'bot_safe_reached')
time.sleep(5)
uid = safe['uid']
before = sample('before', uid)
mark = rows()[-1]['sequence']
(RUN / 'udp-control.json').write_text(json.dumps(dict(id='bot007-controller-cut',
    kind='drop_window', direction='client_to_server', seconds=20)) + '\n')
handoff = wait(lambda r: r.get('kind') == 'gameplay_handoff_complete', after=mark, seconds=90)
time.sleep(15)
after = sample('after', uid)
events = rows()
assert sum(r.get('action') == 'bot_behavior_begin' for r in events) == 1
assert sum(r.get('action') == 'bot_loot_pickup' for r in events) == 2
gun_before = next(x for x in before['equipment_slots'] if x['slot'] == 1)
gun_after = next(x for x in after['equipment_slots'] if x['slot'] == 1)
assert gun_before['definition'] == gun_after['definition'] == 10402
assert gun_before['instance_uid'] == gun_after['instance_uid']
assert before['hp'][0] == after['hp'][0] == 1000
print('native same NPC/gun UID/HP after handoff, behavior did not restart', flush=True)
mark = events[-1]['sequence']
enqueue(RUN / 'live-commands.json', dict(id='bot007-death', action='damage_npc', damage=1000))
dead = wait(lambda r: r.get('kind') == 'live_state_action' and r.get('id') == 'bot007-death', after=mark, seconds=15)
assert dead.get('accepted') and dead['hp'] == 0, dead
items = dead['corpse']['items']
assert {(x['definition'], x['quantity']) for x in items} == {(10402, 1), (30004, 6)}, items
gun = next(x for x in items if x['definition'] == 10402)
assert gun['instance_uid'] == gun_before['instance_uid'] and gun['clip'] == 2
selected = [{k: v for k, v in r.items() if k not in ('remote', 'previous_remote', 'raw', 'hex')}
            for r in rows() if r.get('kind') in ('actor_probe', 'live_state_action', 'gameplay_handoff_complete',
                'winter_kit_initialized', 'death_parcel_probe')]
(HERE / 'native007-result.json').write_text(json.dumps(dict(before=before, after=after,
    handoff=handoff, death=dead, events=selected), indent=2) + '\n')
print('death inventory after handoff: same Citori clip2 + 6 shells; no player starter duplicates', flush=True)
