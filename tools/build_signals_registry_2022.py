"""Единый реестр2022 из адресных ссылок исходников peer и плана механик.

AST-ссылки — кандидаты, а не доказанные wire-контракты. Справочник не
исполняет модули, не читает ключи/трафик и не запускает клиент.
"""
import argparse
import ast
from collections import defaultdict
import csv
import datetime
import hashlib
from pathlib import Path
import re

BUILD = '2022-0.2.989.0-x64'
EXE_SHA = '2dca9b1e122e21363e14eeeb2372598c773205a907ed8d2b2d54a7229ad6ba18'
FIELDS = ('signal_id', 'build', 'exe_path', 'exe_sha256', 'layer', 'opcode_hex',
          'opcode_dec', 'name', 'direction', 'phase', 'schema', 'native_decoder_va',
          'native_handler_va', 'manual_mode', 'manual_example', 'preconditions',
          'server_state_required', 'expected_result', 'verification', 'limitations',
          'mechanic_ids', 'source_refs', 'source_sha256', 'evidence_refs', 'next_step',
          'chain_refs', 'chain_status', 'state_target', 'updated')

# Названия здесь описательные, не восстановленные имена исходного SDK.
# Только адреса/схемы, проверенные в выбранных первичных файлах.
REVIEWED = {
    0x6f55: ('Состояние двери / сущности', 'S2C', 'Проверенный минимум16байт >IBBBBQ id,state,0,0,0,0; count/name пустые; полная схема отдельно', '0x140c9e730'),
    0x6f57: ('Запрос взаимодействия с дверью', 'C2S', '8байт >II entity,state; modeled0/1/2, native open1; не переключать повторно', '0x140be79d0'),
    0x6f58: ('Неактивный обработчик семейства сущностей', 'S2C', 'Wire-схема не установлена; handler возвращает0', ''),
    0x25: ('Движение сущности', 'S2C', '38+12*N; N<=20; см. decode_bc_move', '0x140c59870'),
    0x27: ('Синхронизация позиции', 'S2C', '40 байт; >QiiiBBBIIIBI', '0x140c5a0e0'),
    0x2a: ('Запрос движения', 'C2S', '27+28*N; N<=20; см. decode_move_request', '0x140c56410'),
    0x2b: ('Состояние actor / FSM', 'S2C', 'Контрольный fixture: >QI; значения FSM требуют контекста', ''),
    0x47a: ('Подготовка сцены', 'S2C', '4 байта; >I', '0x140bcd260'),
    0x481: ('Этап закрытия зон', 'S2C', 'encode_shrink; списки future/previous и время этапа', '0x140c3cd80'),
    0x482: ('Длительность выбора', 'S2C', '4 байта; >I selection_seconds', '0x140bcd260'),
    0x483: ('Запрос подготовки', 'C2S', '1 байт; >B; смысл байта не установлен', '0x140bcd1f0'),
    0x484: ('Синхронизация времени подготовки', 'S2C', '8 байт; >II', '0x140c27d10'),
    0x486: ('Прогресс загрузки игроков', 'S2C', '8 байт; >II loaded,total', '0x140c27d10'),
    0x49c: ('Запрос перезарядки', 'C2S', 'Проверяемая ветка:4 байта; WeaponState.handle', ''),
    0x49d: ('Ответ перезарядки', 'S2C', '8 байт; >II slot,0 в нашей ветке', ''),
    0x49e: ('Запрос руки/оружейного слота', 'C2S', '4 байта; WeaponState.handle', ''),
    0x49f: ('Синхронизация руки', 'S2C', '8 байт; >II slot,0 в нашей ветке', ''),
    0x4a0: ('Синхронизация магазина', 'S2C', 'WeaponState.ammunition_sync; не подменять bag/reserve одним HUD', ''),
    0x516: ('Параметр вместимости', 'S2C', 'Контрольная ветка: >HBII', ''),
    0x533: ('Смерть сущности', 'S2C', 'Контрольная ветка: >IQ 0,UnitUID', ''),
    0x547: ('Снаряжение actor', 'S2C', 'ActorFixture.equipment; структура частично восстановлена', ''),
    0x5fb: ('Инвентарь', 'S2C', 'WeaponState.inventory; состав контейнеров зависит от состояния', ''),
    0x6f5: ('Вес сумки', 'S2C', '4 байта; >I; целая часть веса нашего bag', ''),
    0x821: ('Создание наземного предмета', 'S2C', 'Контроль100байт: UID@4; >3i XYZ@29; >III def,qty,index@63', '0x140c30740'),
    0x82b: ('Удаление наземного предмета', 'S2C', '8 байт; >Q entity_uid', ''),
    0xdce: ('Запрос входа в комнату', 'C2S', '20 байт; >QIQ', '0x140c3a870'),
    0x1069: ('HP actor', 'S2C', 'Контроль19байт: >QBBBII UID,0,1,0,current,maximum; общий decoder: count<=19 записей по9байт; RawHP1000=100HUD в профиле', '0x140be1e60'),
    0x106a: ('Массив атрибутов actor', 'S2C', '1080байт;120 записей >BII; семантика части слов неизвестна', '0x140c2ad90'),
    0x11ea: ('SHOOT_TARGET_RSP: legacy feedback с проверкой EuRPG', 'S2C', '36байт: >IQIII +8bytes +I; target@4,damage@32; неизвестные поля не выдавать за полный контракт', '0x140c41120'),
    0x11eb: ('SHOOT_TARGET_BC_SYNC: попадание/штатный hitmarker', 'S2C', '48байт >QQ3iBBIBB3I shooter,target,relativeXYZ,POS-tail,part,damage,dead,articulo,tick,offsetms,weaponID', '0x140c413f0'),
    0x0bfc: ('Выбор начального комплекта: legacy request', 'C2S', '4байта >I choice1/2/3 до дедлайна подготовки; choose_winter_kit', ''),
    0x0bfd: ('Подтверждение начального комплекта: legacy response', 'S2C', '8байт >II error,choice в проверенной ветке peer', ''),
    0x10cc: ('Запрос изменения raw-атрибута', 'C2S', '8байт >II index,value; index1 выбирает начальный комплект1/2/3 до первого5FB', ''),
    0x10cd: ('Ответ изменения raw-атрибута', 'S2C', '12байт >III index,value,error; error0 accepted/1 rejected в проверенной ветке peer', ''),
    0x10d0: ('Обновление raw-атрибута', 'S2C', '8байт >II index,value; index1 выбор комплекта;2/3/4 маски способности;5 signed-int32 temperature_raw в0.01°C; другие индексы отдельно', ''),
    0x11df: ('Запрос выбора клетки появления', 'C2S', '24байта >IQIII kind,actorUID,cellX,cellY,trailing; принят kind2/ownUID/X,Y0..31/trailing0..1 до дедлайна; смысл остальных вариантов не установлен', ''),
    0x11e0: ('Снимок выбранной клетки появления', 'S2C', 'Контроль8+20*N: >II count,bornType затем N записей >QIII actorUID,cellX,cellY,0; проверены N0/type2 initial и N1/type2 selected', ''),
    0x11e2: ('Правила подготовки выбора появления', 'S2C', 'Контроль12байт >III bornType2,0,0; семантика двух последних слов не установлена', ''),
    0x11da: ('Запрос выстрела', 'C2S', 'Проверяемая ветка49байт; WeaponState.handle', ''),
    0x11dd: ('Сообщение попадания с направлением', 'C2S', '104фиксированных байта + countBE16@104 + 19*Nsurface + 10*Nunit (count<=30): targetUID@4, gunXYZ@25, targetXYZ@37, impactXYZ@50; chPart_id@62; target pathID@71/seq75/use_c76/on_vehicle77; shooter pathID@78/seq82/use_c83; iBullet_id@88/iRatio@92/iPellet_index@100. Поле83 не headshot; part_id HEAD1/BODY2/LIMB3; tag0 >BBBI3f, tag1 >BQB', '0x140c3fe00'),
    0x3b61: ('Содержимое контейнера лута', 'S2C', 'ParcelState.contents; не эквивалент821', ''),
    0x3b63: ('Запрос подбора предмета', 'C2S', 'Проверяемая ветка33байта; index/slot/distance и registry', ''),
    0x3b64: ('DROP_MSGID_RSP_PICK: ответ подбора', 'S2C', 'Контроль45байт из WeaponState.handle(0x3b63): >IIIBI +28zero: index,u32_4,quantity,union_tag1,definition; tail28 неизвестен. Callback decoded prefix4: dropID+4/qty+0xC/definition+0x11; не wire offsets', ''),
    0x3e80: ('Перенос предмета / сохранение экипировки', 'C2S', 'WeaponState.move_item и local_clothing; сценарии различаются', ''),
    0x3e81: ('Подтверждение переноса', 'S2C', 'Контрольная ветка: >BIIB; флаги зависят от операции', ''),
    0x3e82: ('Изменение слота инвентаря', 'S2C', 'encode_delta; container,slot,itemdata; снимок != команда выдачи', ''),
    0x4816: ('Часы окружения', 'S2C', '8байт; >II hour,UNIXseconds; не tick', ''),
    0x6541: ('Запрос посадки в транспорт', 'C2S', 'VehicleState.handle; UID/место проверяются', ''),
    0x6542: ('Ответ посадки', 'S2C', 'VehicleState.handle; соответствующий fixture', ''),
    0x6543: ('Запрос выхода из транспорта', 'C2S', 'VehicleState.handle; только текущая посадка', ''),
    0x6544: ('Ответ выхода', 'S2C', 'VehicleState.handle; соответствующий fixture', ''),
    0x6547: ('Запрос смены места', 'C2S', 'VehicleState.handle; допустимость места зависит от транспорта', ''),
    0x6548: ('Ответ смены места', 'S2C', 'VehicleState.handle; соответствующий fixture', ''),
    0x6554: ('HP/статус транспорта', 'S2C', '16байт; >QII vehicleUID,hp,status', ''),
    0x656f: ('Запрос открытия контейнера', 'C2S', 'ParcelState.handle; наличие/дистанция/contents', ''),
    0x6575: ('Позиция транспорта', 'C2S/S2C', 'Проверяемый fixture73байта; различать owner/relay', ''),
}


def command_references(path, relative):
    """Находим только явные сравнения command и пары(hex opcode,payload).

    Это индекс для ручной проверки: сравнение может относиться к fixture,
    а не входящему сообщению, поэтому направление автоматически не задаём.
    """
    text = path.read_text(encoding='utf-8-sig')
    tree = ast.parse(text)
    references = defaultdict(set)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node) or ''
            for literal in re.findall(r'0x([0-9a-fA-F]{1,4})(?![0-9a-fA-F])', doc):
                code = int(literal, 16)
                if code in REVIEWED:
                    references[code].add(f'{relative}:{node.body[0].lineno}')
        constants = []
        if isinstance(node, ast.Compare):
            values = [node.left, *node.comparators]
            if not any(isinstance(v, ast.Name) and v.id in ('command', 'code', 'opcode')
                       or isinstance(v, ast.Attribute) and v.attr == 'command' for v in values):
                continue
            constants = [v for value in values for v in ast.walk(value) if isinstance(v, ast.Constant)]
        elif isinstance(node, ast.Tuple) and len(node.elts) == 2:
            constants = node.elts[:1]
        for value in constants:
            if not isinstance(value, ast.Constant) or type(value.value) is not int or not 0 < value.value <= 65535:
                continue
            literal = ast.get_source_segment(text, value) or ''
            if not literal.lower().startswith('0x'):
                continue
            references[value.value].add(f'{relative}:{value.lineno}')
    return references, hashlib.sha256(path.read_bytes()).hexdigest()


def build(workspace, as_of=None):
    workspace = Path(workspace)
    as_of = as_of or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    datetime.date.fromisoformat(as_of)
    refs, hashes = defaultdict(set), {}
    paths = sorted((workspace / 'server/directory').glob('*2022.py'))
    paths += [workspace / 'tools' / name for name in
              ('roe_scene_2023.py', 'roe_room_2023.py', 'local_clothing_2022.py')]
    for path in paths:
        relative = path.relative_to(workspace).as_posix()
        found, digest = command_references(path, relative)
        for code, sources in found.items():
            refs[code].update(sources)
        hashes[relative] = digest
    for code in (0x6f55, 0x6f57, 0x6f58):
        primary = 'docs/AUTO-DOORS-20261013.md'
        refs[code].add(primary + ':1')
        hashes[primary] = hashlib.sha256((workspace / primary).read_bytes()).hexdigest()
    with (workspace / 'docs/recovery/mechanics-2022.csv').open(encoding='utf-8-sig', newline='') as stream:
        mechanics = list(csv.DictReader(stream, delimiter=';'))
    rows = []
    for code in sorted(set(refs) | set(REVIEWED)):
        reviewed = REVIEWED.get(code)
        linked = [r for r in mechanics if any(re.fullmatch(r'(?:0x)?[0-9a-fA-F]{2,4}', s)
                  and int(s, 16) == code for s in re.split(r'[;,|\s]+', r['signals']))]
        row = dict.fromkeys(FIELDS, '')
        row.update(signal_id=f'SIG2022-OP-{code:04X}', build=BUILD,
                   exe_path='Ring of Elysium-2022/Europa_Client.exe', exe_sha256=EXE_SHA,
                   layer='application' if reviewed else 'не установлен',
                   opcode_hex=f'0x{code:04X}', opcode_dec=str(code),
                   name=reviewed[0] if reviewed else 'Кандидат из ссылок peer; семантика не проверена',
                   direction=reviewed[1] if reviewed else 'не установлено',
                   phase='матч/подготовка; уточнить условия обработчика',
                   schema=reviewed[2] if reviewed else 'Не установлена; перейти к source_refs',
                   native_decoder_va=reviewed[3] if reviewed else '',
                   manual_mode='state_handler_or_fixture' if reviewed else 'research_only',
                   preconditions='Активная совместимая сессия и нужные UID/контейнеры; проверять обработчик',
                   server_state_required='да; изменение состояния отдельно от wire/UI',
                   expected_result=reviewed[0] if reviewed else 'Не установлен',
                   verification='reviewed_source; динамику см.evidence_refs' if reviewed else 'source_reference_only',
                   limitations='Не является полным SDK/списком сигналов игры; названия описательные; Windows и исходный сервер отдельно',
                   mechanic_ids='|'.join(r['id'] for r in linked),
                   source_refs='|'.join(sorted(refs[code])),
                   source_sha256='|'.join(f'{p}={hashes[p]}' for p in sorted({s.rsplit(':', 1)[0] for s in refs[code]})),
                   evidence_refs='|'.join(sorted({v for r in linked for v in r['evidence'].split('|') if v})),
                   next_step='Проверить native/UI/серверное состояние отдельно; добавить typed action' if reviewed else 'Установить слой, направление, имя и wire-схему; затем адресный native-повтор',
                   updated=as_of)
        if code in (0x6f55, 0x6f57, 0x6f58):
            row['evidence_refs'] = 'docs/AUTO-DOORS-20261013.md|research/builds/2022/recovery/015-loot01/20261013-auto-doors/report.md'
            row['limitations'] = 'Proton369 ordinaryopen1/insidepickup;370 UDP20s door1 preserved;372 diagnostictransfer/Fopen2/close0/upperpickup; ordinary upstairs route/shared room/Windows pending'
            if code == 0x6f55:
                row['native_handler_va'] = '0x1413543d0 ->0x141354090 ->0x1409abe50'
                row['manual_mode'] = 'state_handler_with_door_config; diagnostic_wire_helper separately'
                row['manual_example'] = 'python tools/entity_status_action_2022.py --run RUN --entity-id 7767 --state open --id door-open-1'
                row['server_state_required'] = 'да; DoorState authoritative singleton; raw helper реестр не изменяет'
                row['verification'] = 'native decoder/consumer + visual open/close + passage/pickup'
                row['state_target'] = 'DoorState.status[entity_id] -> native entity+0x98'
            if code == 0x6f58:
                row['native_handler_va'] = '0x14019b8f0'
                row['manual_mode'] = 'research_only'
                row['verification'] = 'native return0; полезное действие не подтверждено'
                row['expected_result'] = 'В данном handler действие отсутствует'
        if code == 0x821:
            row['limitations'] = 'Native372 wire42 float0/pi2/122 -> componentF9; model rotation/matrix unchanged. Назначение/units/Direction binding иWindows отдельно'
            row['evidence_refs'] += '|docs/LOOT-GROUND-CONSUMER-20261013.md|research/builds/2022/recovery/031-loot09/20261013-direction-consumer/ground-selected-direction122.json'
            row['next_step'] = 'Producer821 или другая entity-ветка с подтверждённым применением float42 вtransform'
        if code == 0x11dd:
            primary = 'docs/HIT-FIELDS-20261015.md'
            row['source_refs'] += '|'+primary
            row['source_sha256'] += '|'+primary+'='+hashlib.sha256((workspace/primary).read_bytes()).hexdigest()
            row['evidence_refs'] += '|research/builds/2022/recovery/076-ops02/20261015T1432-windows-feedback/hit-field-bindings.json'
            row['limitations'] = 'Имена/смещения из SWIG getters и decoder2022; path_use_c не headshot. Значения part_id и исходная формула урона/брони не восстановлены'
            row['next_step'] = 'Проследить producer chPart_id@62 и кости коллизии; нужны положительные head/body trace с фиксированными оружием/позицией/impact'
        if code == 0x1069:
            row['native_handler_va'] = '0x1412ebcf0'
        if code in (0x0bfc, 0x0bfd, 0x10cc, 0x10cd, 0x10d0, 0x11df, 0x11e0, 0x11e2):
            primary = 'research/builds/2022/recovery/windows-20261014-c6ada6/report.md'
            if (workspace/primary).exists():
                row['source_refs'] += '|'+primary
                row['source_sha256'] += '|'+primary+'='+hashlib.sha256((workspace/primary).read_bytes()).hexdigest()
                row['evidence_refs'] = '|'.join(filter(None, (row['evidence_refs'],
                    'research/builds/2022/recovery/windows-20261014-c6ada6/native-checks.json')))
            ids = set(row['mechanic_ids'].split('|'))-set(('',))
            ids.add('KIT01')
            row['mechanic_ids'] = '|'.join(sorted(ids))
            row['phase'] = ('подготовка и активный матч' if code == 0x10d0
                            else 'подготовка до первого5FB и дедлайна selection')
            row['verification'] = ('modeled legacy BFC/BFD; UI использует10CC/10CD/10D0'
                if code in (0x0bfc, 0x0bfd) else
                'native UI cold132-134 и001-004; клиентские запросы/peer responses и source InitItem')
            row['limitations'] = 'Исходный server policy/initial magazine/полные варианты сообщения не восстановлены; Windows12rejected11DF безpayloadfields; native114accepted без воспроизведения паузы5с; полный DLL→handler путь неизвестен'
            if code == 0x11df:
                row['next_step'] = 'Получить numeric kind/UID-match/X/Y/trailing в новом Windows rejection; не ослаблять guard без первичных данных'
                row['state_target'] = 'state.born_point; обе own27 получают выбранныйXYZ; marker подтверждает cell через11E0'
            elif code in (0x10cc, 0x0bfc):
                row['state_target'] = 'state.winter_choice → selected_fixture перед первым5FB → source starter items и kit_sync'
        if reviewed and row['direction'] == 'C2S':
            row['manual_mode'] = 'client_request; не команда server_to_client'
        rows.append(row)
    for action, parameter, limit, result in (
        ('set_own_health', '--hp 850', '1..HPначального профиля; не оживляет dead', 'HP850≈85HUD'),
        ('give_ammo', '--definition 30004 --quantity 6', '1..100; def30004/30001/30002/30005; вся пачка должна помещаться', 'Bag/reserve увеличиваются на6'),
        ('damage_npc', '--damage 100', '1..1000raw; живой started NPC; учебная armor formula', 'HP NPC уменьшается; при смерти current death loot')):
        row = dict.fromkeys(FIELDS, '')
        row.update(signal_id='SIG2022-ACT-'+action.upper(), build=BUILD,
                   exe_path='Ring of Elysium-2022/Europa_Client.exe', exe_sha256=EXE_SHA,
                   layer='administrative_action', name=action, direction='operator→local_peer',
                   phase='активный одиночный матч', schema=limit, manual_mode='typed_action',
                   manual_example=f'.\\.tools\\python\\python.exe -B .\\tools\\scene_action_2022.py --run RUN_DIR --id UNIQUE_ID --action {action} {parameter}',
                   preconditions='Запуск с -LiveControl; текущий RUN_DIR; уникальныйID; alive WorldState/WeaponState',
                   server_state_required='да; controller обновляет состояние и создаёт сообщения',
                   expected_result=result, verification='Proton318; административный controller',
                   limitations='Не opcode и не оригинальная консоль; enqueue не подтверждает применение; Windows отдельно',
                   mechanic_ids='OPS04', source_refs='server/directory/state_scene_actions_2022.py|server/directory/live_scene_probe_2022.py',
                   source_sha256='server/directory/state_scene_actions_2022.py='+hashes['server/directory/state_scene_actions_2022.py'],
                   evidence_refs='docs/STATE-CONTROL-20261012.md|docs/OPS04-STATE-ACTIONS-20261012.md',
                   next_step='Искать live_state_action поID иaccepted/reason; сверить клиентское и серверное состояние', updated=as_of)
        rows.append(row)
    # Явные источники цепочек: новый native опыт уточняет прежний архивный разбор.
    for relative in ('research/builds/2022/module-signal-map-20261013/signal-chains.csv',
                     'research/builds/2022/recovery/011-net06/20261013-native-magazine/signal-chains.csv'):
        chain_path = workspace/relative
        if chain_path.exists():
            with chain_path.open(encoding='utf-8-sig',newline='') as stream:
                chains = list(csv.DictReader(stream,delimiter=';'))
            for row in rows:
                matched = [step for step in chains if step['signal_id'] == row['signal_id']]
                if not matched:
                    continue
                row['chain_refs'] = '|'.join(sorted({chain_path.relative_to(workspace).as_posix()+'#'+s['chain_id'] for s in matched}))
                row['chain_status'] = 'partial; receive→decoder и полный dispatcher не установлены'
                row['state_target'] = '|'.join(s['state_effect'] for s in matched if s['state_effect'])
                row['source_sha256'] += '|'+chain_path.relative_to(workspace).as_posix()+'='+hashlib.sha256(chain_path.read_bytes()).hexdigest()
                for step in matched:
                    if step['stage'] == 'handle' and step['module'] == 'Europa_Client.exe':
                        row['native_handler_va'] = step['va']
                    if step['stage'] == 'decode' and step['module'] == 'Europa_Client.exe':
                        row['native_decoder_va'] = step['va']
                if row['opcode_hex'] == '0x04A0':
                    row['schema'] = 'Контроль20байт: >QIII actorUID,slot,clip,counter; counter не bag reserve'
    for row in rows:
        if row['opcode_hex'] not in ('0x11DD', '0x11EA', '0x11EB'):
            continue
        primary = 'docs/HIT-FEEDBACK-20261016.md'
        if not (workspace/primary).exists():
            continue
        row['source_refs'] += '|'+primary
        row['source_sha256'] += '|'+primary+'='+hashlib.sha256((workspace/primary).read_bytes()).hexdigest()
        row['evidence_refs'] += '|research/builds/2022/recovery/050-inv07/20261015T2337-ground-attachment/evidence.json'
        if row['opcode_hex'] == '0x11DD':
            row['limitations'] = 'Native005 part1 при прицельном headhit; part2/3 обычные. Поле83 shooter_path_use_c, не headshot. Исходный damage multiplier не восстановлен'
            row['next_step'] = 'Server material/thickness validation, исходный authoritative hurt; Windows W17'
            extra = 'docs/HIT-RECORDS-20261016.md'
            if (workspace/extra).exists():
                row['source_refs'] += '|'+extra
                row['source_sha256'] += '|'+extra+'='+hashlib.sha256((workspace/extra).read_bytes()).hexdigest()
                row['evidence_refs'] += '|research/builds/2022/recovery/043-gun06/20261016T0300-native-obstacle/native017-extended-hit-validation.json'
                row['verification'] = 'native017 genuine AK through Rock305:144/count2→HP900→800/11EB/UI/Wwise; native codec union0/1 и7regressions'
                row['limitations'] = 'Part HEAD1/BODY2/LIMB3;83 shooter_path_use_c. Хвост telemetry, не authority. Урон100 учебный; исходная HP/head/armor формула и server penetration открыты'
                row['chain_refs'] += '|'+extra
                row['state_target'] = 'ActorState/SharedCombat принимает известные записи до30, один accepted hit→HP/armor/dedup/11EB; записи не умножают урон'
            continue
        row.update(phase='активный матч после принятого попадания',
            native_handler_va='0x14130fd50' if row['opcode_hex'] == '0x11EA' else '0x14130ffa0',
            limitations='Урон/броня/LOS учебные; Windows/LAN и слышимый аудиовыход отдельно',
            next_step='Windows W17; исходный баланс отдельно GUN07')
        if row['opcode_hex'] == '0x11EA':
            row.update(expected_result='M4/QSRifle выходит на type-chain; штатные отметки требуют11EB',
                verification='native002 hardware type gate; primary init EuRPG/QSRifle',
                chain_status='handler/type gate подтверждены; успешный RPG отдельно')
        else:
            row.update(manual_mode='accepted_hit_state_handler',
                preconditions='Принятый серверный выстрел/hit, живой target; shooterUID текущей сессии',
                expected_result='Белый/body, оранжевый/armor, красный/dead; part1 head feedback и отдельный звук',
                verification='native005 body/head/miss;006 armor/dead; decoder48/short47 и штатные UI/Wwise',
                mechanic_ids='GUN05|GUN07|HP03|MP03',
                chain_refs='docs/HIT-FEEDBACK-20261016.md',
                chain_status='decode→handler→component→EventPlayerHitTarget→OnHitTarget/Wwise подтверждено',
                state_target='HP/armor/dedup изменяет ActorState;11EB уведомляет штатную панель/эффект')
    review = 'docs/WINDOWS-W17-REVIEW-20261016.txt'
    if (workspace/review).exists():
        for row in rows:
            if row['opcode_hex'] != '0x11EB':
                continue
            row['source_refs'] += '|'+review
            row['source_sha256'] += '|'+review+'='+hashlib.sha256((workspace/review).read_bytes()).hexdigest()
            row['evidence_refs'] += '|research/builds/2022/recovery/076-ops02/20261016T134206-w17-review/evidence.json'
            row['verification'] += '; Windows134206-fafd00 user audible/body/head/kill,13accepted11EB'
            row['limitations'] = 'Урон/броня/LOS учебные; Windows legacy UI/звук подтверждены user+export; public упаковка и Windows through-hit отдельно'
            row['next_step'] = 'Native full-magazine reload visual fix GUN02/W18; original hurt GUN07 отдельно'
    capacity = 'docs/RELOAD-CAPACITY-20261016.md'
    if (workspace/capacity).exists():
        for row in rows:
            if row['opcode_hex'] not in ('0x049C', '0x049D', '0x04A0', '0x3E82'):
                continue
            row['source_refs'] += '|'+capacity
            row['source_sha256'] += '|'+capacity+'='+hashlib.sha256((workspace/capacity).read_bytes()).hexdigest()
            row['evidence_refs'] += '|research/builds/2022/recovery/035-gun02/20261016T1520-fullmag/native021-public-events.json'
            row['verification'] += '; Native021 fullR gate17/17, partial16→17; M4/AK30, extended40'
            row['limitations'] += '; новая полнаяR исправлена по native capacity; WindowsW18 ещё отдельно, старый Citori374 handoff не закрыт'
            row['next_step'] = 'WindowsW18 full/partialR; остальные семейства и handoff отдельно'
            if row['opcode_hex'] == '0x3E82':
                row['state_target'] += '; gun ITEM_DATA+54 BE32/ref+56→native gun+810 capacity, включая расширитель'
    reviews = [
        ('docs/INVENTORY-BRANCH-CONTROL-20261018.md', {'0x3B64', '0x3E82'}),
        ('docs/PASSIVE-TARGETS-20261018.md', {'0x0533', '0x0565', '0x0BE7', '0x11DD', '0x11EB', '0x3B61'}),
        ('docs/NET06-CAPACITY-HANDOFF-20261018.md', {'0x049C', '0x049D', '0x049E', '0x049F', '0x04A0'}),
    ]
    for reference, codes in reviews:
        if not (workspace/reference).exists():
            continue
        for row in rows:
            if row['opcode_hex'] not in codes:
                continue
            row['source_refs'] += '|' + reference
            row['source_sha256'] += '|' + reference + '=' + hashlib.sha256((workspace/reference).read_bytes()).hexdigest()
            row['evidence_refs'] += '|' + reference
            if row['opcode_hex'] == '0x3B64':
                row['native_handler_va'] = '0x140D629A0'
                row['chain_status'] = 'registration_callback_static; decoder_unknown'
                row['verification'] += '; регистрация140D61EAA–140D61ECD, callback статически проверен2022'
                row['limitations'] += '; native trace callback3B64/decoder ещё отсутствует'
            elif row['opcode_hex'] == '0x3E82':
                row['native_handler_va'] = '0x140E162D0'
                row['chain_status'] = 'native_flag1_branch_confirmed; partial_state_mapping'
                row['state_target'] += '; decoded flag+0xA285/UID+0xA286; flag1 cache140F48330/inventory+130'
                row['verification'] += '; Native003 flag1 hardware branch; Native004 flag0 отрицательный и отменён'
                row['limitations'] += '; визуальная задержка3D не исправлена; decoded offsets не wire'
                row['next_step'] = 'Read-only3B64→inventory→UI-model на успешном/задержанном pickup; flag1 сохранить'
            elif reference.endswith('PASSIVE-TARGETS-20261018.md'):
                row['verification'] += '; Native002 два genuine M4 kills/раздельные сумки;005 десять admin deaths/handoff'
                row['limitations'] += '; группа пассивная, фиксированные точки; admin deaths не gun kills; WindowsW19 отдельно'
            else:
                row['verification'] += '; Native001 M4/Glock/AK pendingR+C2SUDP20s/следующийfireR; earlyfire и switch'
                row['limitations'] += '; Citori374 остаётся открыт; WindowsW19 отдельно'
                row['next_step'] = 'WindowsW19; Citori374 повторить только с воспроизводимым отрицательным контролем'
    for row in rows:
        if row['signal_id'] != 'SIG2022-ACT-DAMAGE_NPC':
            continue
        reference = 'docs/LIVE-COMMAND-LIFETIME-20261018.md'
        if not (workspace/reference).exists():
            continue
        row['schema'] += '; optional npc_uid U64 адресует конкретную пассивную мишень; без поля первая'
        row['manual_example'] += ' --npc-uid 0x2040000800007'
        row['preconditions'] += '; новыйID для каждого действия, включая новый матч; без --id генерируется автоматически'
        row['verification'] += '; Native005 десять независимых UID/20admin actions; lifecycle ID unit-tested'
        row['limitations'] += '; не добавляет gun kills; ledger живёт до остановки peer, не durable account storage'
        row['source_refs'] += '|' + reference
        row['evidence_refs'] += '|docs/PASSIVE-TARGETS-20261018.md'
    chain = 'docs/PICK-DECODE-CHAIN-20261018.md'
    if (workspace/chain).exists():
        for row in rows:
            if row['opcode_hex'] not in ('0x3B64', '0x3E82'):
                continue
            row['native_decoder_va'] = ('0x140C69B00' if row['opcode_hex'] == '0x3B64' else '0x140C4BA10')
            row['chain_status'] = 'native_decoder_and_handler_confirmed; upstream_static_edges'
            row['chain_refs'] += '|' + chain
            row['source_refs'] += '|' + chain
            row['source_sha256'] += '|' + chain + '=' + hashlib.sha256((workspace/chain).read_bytes()).hexdigest()
            row['evidence_refs'] += '|research/builds/2022/recovery/022-inv02/20261018T1230-pick-handler/native011-decode-chain.log'
            row['verification'] += '; Native010/011 actual pickup: body decoder→same decoded object→callback;3E82 decoder entry/handler/cache'
            row['limitations'] += '; все эти адреса в rootEXE; UI-model задержка ещё не исправлена, не полный SDK'
            row['limitations'] = row['limitations'].replace(
                '; native trace callback3B64/decoder ещё отсутствует',
                '; прежнее отсутствие trace закрыто Native010/011')
            row['next_step'] = 'Read-only consumer/UI-model notification после cache на успешном/задержанном pickup; flag1 сохранить'
    material = 'docs/M4-THROUGH-ROCK-20261018.md'
    if (workspace/material).exists():
        for row in rows:
            if row['opcode_hex'] not in ('0x11DD', '0x11EB'):
                continue
            row['source_refs'] += '|' + material
            row['source_sha256'] += '|' + material + '=' + hashlib.sha256((workspace/material).read_bytes()).hexdigest()
            row['evidence_refs'] += '|research/builds/2022/recovery/043-gun06/20261018T1155-m4-edge/native009-through-hit.json'
            row['verification'] += '; Native009 genuineM4through24.04757cm/count2/nativeHP700; sourcepoints<=0.04128cm'
            row['limitations'] += '; energy8.63385 calculated from known branch, not new hardware energy; oneRock opt-in'
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--as-of', help='Дата обновления ISO8601; по умолчанию текущая UTC')
    args = parser.parse_args(argv)
    rows = build(args.workspace, args.as_of)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, FIELDS, delimiter=';', lineterminator='\r\n')
        writer.writeheader()
        writer.writerows(rows)
    print(f'Строк:{len(rows)}; reviewed:{len(REVIEWED)}; typed_actions:3; остальные — кандидаты')


if __name__ == '__main__':
    main()
