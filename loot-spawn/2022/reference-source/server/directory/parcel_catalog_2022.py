"""Несколько диагностических контейнеров: независимый pickup патронов и equipment.

Wire 654b/6571/3b61/3b64 взят из проверенных одиночных опытов. Состав,
расположение и расписание задаются явно; нативный генератор не восстановлен.
"""
from dataclasses import dataclass, replace
import json
from pathlib import Path
import struct

from parcel_probe_2022 import ParcelFixture, ParcelState
from weapon_probe_2022 import AMMUNITION_WEIGHTS, EQUIPMENT_SLOTS, LootFixture


@dataclass(frozen=True)
class ContainerFixture:
    uid: int
    index: int
    position: tuple
    items: tuple
    native_motion: bool = False


@dataclass(frozen=True)
class ParcelCatalog:
    containers: tuple

    @classmethod
    def load(cls, path, weapon, catalog=None):
        path = Path(path)
        if not weapon or not weapon.all_loot:
            raise ValueError('Несколько контейнеров требуют проверенный ground821 из weapon-config')
        config = json.loads(path.read_text())
        rows = config['parcels']
        if not isinstance(rows,list) or not 1 <= len(rows) <= 16:
            raise ValueError('Нужно 1..16 контейнеров')
        template = weapon.all_loot[0].entity
        if len(template) != 100:
            raise ValueError('Нужен шаблон ground821 из проверенной fixture')
        known = tuple(weapon.all_loot) + (catalog.items if catalog else ())
        indexes, uids = {x.index for x in known}, {x.entity_uid for x in known}
        container_ids, containers = set(), []
        for row in rows:
            native_motion = row.get('native_motion', False)
            if type(native_motion) is not bool:
                raise ValueError('native_motion должен быть bool')
            source = path.parent / row['entity_file']
            if source.stat().st_size != 117:
                raise ValueError('Нужна модель зимнего аирдропа 654b/501, 117 байт')
            body = source.read_bytes()
            uid, definition = struct.unpack_from('>QI',body)
            index = row['parcel_id']
            if (not uid or uid in uids or definition != 501
                    or type(index) is not int or not 1 <= index <= 0xffffffff
                    or index in container_ids or index in indexes):
                raise ValueError('Повторный или неверный контейнер')
            position = tuple(struct.unpack_from('>3i',body,20))
            records = row['items']
            if not isinstance(records,list) or not 1 <= len(records) <= 16:
                raise ValueError('Нужно 1..16 предметов контейнера')
            container_ids.add(index); uids.add(uid)
            items = []
            for record in records:
                item_index, item_definition, quantity = (record['item_index'],
                                                        record['definition'],record['quantity'])
                if (type(item_index) is not int or not 1 <= item_index <= 0xffffffff
                        or item_index in indexes or item_index in container_ids
                        or type(item_definition) is not int
                        or item_definition not in (*AMMUNITION_WEIGHTS,*EQUIPMENT_SLOTS)
                        or type(quantity) is not int or not 1 <= quantity <= 100
                        or (item_definition not in AMMUNITION_WEIGHTS and quantity != 1)):
                    raise ValueError('Неверный или повторный предмет контейнера')
                # Виртуальный ground-item используется только как авторитетный
                # учёт inventory; его 821 не отправляется клиенту.
                item_uid = 0x00031d0400000000 + item_index
                if item_uid in uids:
                    raise ValueError('Повторный UID предмета')
                entity = bytearray(template)
                struct.pack_into('>Q',entity,4,item_uid)
                struct.pack_into('>3i',entity,29,*position)
                struct.pack_into('>III',entity,63,item_definition,quantity,item_index)
                ack = struct.pack('>IIIBI',item_index,0,quantity,1,item_definition)+bytes(28)
                items.append(LootFixture(item_uid,item_index,quantity,position,ack,
                                         item_definition,bytes(entity)))
                indexes.add(item_index);uids.add(item_uid)
            containers.append(ContainerFixture(uid,index,position,tuple(items),native_motion))
        return cls(tuple(containers))


class ContainerState:
    def __init__(self, fixture):
        self.fixture = fixture
        self.spawned = self.linked = self.opened = False
        self.position = fixture.position
        self.motion_tick = None
        self.registered = False
        self.remaining = {x.index:x.quantity for x in fixture.items}

    def register(self, command, body):
        if (command == 0x654b and len(body) == 117
                and struct.unpack_from('>QI',body) == (self.fixture.uid,501)):
            self.spawned = True
        elif (command == 0x6571 and len(body) == 12
              and struct.unpack('>QI',body) == (self.fixture.uid,self.fixture.index)):
            self.linked = True
        elif (command == 0x654c and len(body) == 8
              and struct.unpack('>Q',body)[0] == self.fixture.uid):
            self.spawned = self.linked = False

    def at_position(self, item):
        entity = bytearray(item.entity)
        struct.pack_into('>3i', entity, 29, *self.position)
        return replace(item, position=self.position, entity=bytes(entity))

    def observe_motion(self, body, weapon):
        """Явный одиночный режим: native501 MOVE_REQ, не серверная физика."""
        if len(body) != 73:
            raise ValueError('native501 MOVE_REQ ожидает73байта')
        tick = struct.unpack_from('>I', body, 8)[0]
        position = struct.unpack_from('>3i', body, 13)
        event = dict(action='parcel_motion_rejected', parcel_id=self.fixture.index,
                     uid=hex(self.fixture.uid), experimental=True)
        if not self.spawned or not self.linked:
            return dict(event, reason='not_spawned')
        origin = self.fixture.position
        # Собственные ограничения стенда; карту/исходный collision server не заменяют.
        if (sum((position[i]-origin[i])**2 for i in (0,1)) > 50000**2
                or not origin[2]-100000 <= position[2] <= origin[2]+1000):
            return dict(event, reason='outside_envelope')
        if self.motion_tick is not None:
            delta = (tick-self.motion_tick) & 0xffffffff
            if not 0 < delta < 0x80000000:
                return dict(event, reason='stale_tick')
            allowance = 20000 * min(delta/25, 40) + 1500
            if sum((a-b)**2 for a,b in zip(position,self.position)) > allowance**2:
                return dict(event, reason='speed')
        self.position, self.motion_tick = position, tick
        if self.registered:
            for item in self.fixture.items:
                old = weapon.loot_registry.get(item.index)
                if old is not None:
                    weapon.loot_registry[item.index] = self.at_position(old)
        return dict(action='parcel_native_motion', parcel_id=self.fixture.index,
                    uid=hex(self.fixture.uid), position=position, client_tick=tick,
                    experimental=True, client_authoritative=True)

    def contents(self):
        entries = [x for x in self.fixture.items if self.remaining[x.index]]
        body = struct.pack('>II',self.fixture.index,len(entries))
        for item in entries:
            body += struct.pack('>8IQ',item.index,1,item.definition,
                                self.remaining[item.index],0,0,0,0,0)
        return body + bytes(4)

    def handle(self, command, body, weapon):
        if command == 0x656f:
            if len(body) != 8:
                raise ValueError('AIR_DROP_OPEN_REQ ожидает 8 байт')
            if not self.spawned or not self.linked:
                return [], dict(action='parcel_open_rejected',parcel_id=self.fixture.index)
            self.opened = True
            return [(0x3b61,self.contents())], dict(action='parcel_open',
                    parcel_id=self.fixture.index,item_count=sum(bool(x) for x in self.remaining.values()))
        if len(body) != 33:
            raise ValueError('PICK_REQ ожидает 33 байта')
        parcel,index,target,byte,short,flag,x,y,z,tail = struct.unpack('>IIQBHB3iB',body)
        item = next((v for v in self.fixture.items if v.index == index),None)
        distance = sum((a-b)**2 for a,b in zip((x,y,z),self.position))
        if (not self.spawned or not self.linked or not self.opened or item is None
                or parcel != self.fixture.index or target or byte or short
                or flag != 1 or tail or distance >= 750**2):
            return [], dict(action='parcel_pick_rejected',parcel_id=self.fixture.index)
        if not self.registered:
            if any(v.index in weapon.loot_registry for v in self.fixture.items):
                raise ValueError('Индекс контейнера занят текущим inventory')
            for v in self.fixture.items:
                weapon.loot_registry[v.index] = self.at_position(v)
                weapon.available_loot.add(v.entity_uid)
            self.registered = True
        converted = struct.pack('>IIQBHB3iB',index,0,target,byte,short,flag,x,y,z,tail)
        packets,event = weapon.handle(0x3b63,converted)
        if event['action'] not in ('pickup','equipment_pickup','duplicate_pickup'):
            return [], dict(action='parcel_pick_rejected',parcel_id=self.fixture.index,
                            inventory_action=event['action'])
        self.remaining[index] = 0 if index in weapon.picked_loot else weapon.loot_registry[index].quantity
        responses = []
        for code,payload in packets:
            if code == 0x82b and payload == struct.pack('>Q',item.entity_uid):
                continue
            if (code == 0x821 and len(payload) == 100
                    and struct.unpack_from('>Q',payload,4)[0] == item.entity_uid):
                # Остаток находится внутри контейнера, а не на земле.
                continue
            if code == 0x3b64:
                payload = struct.pack('>II',parcel,index) + payload[8:]
            responses.append((code,payload))
        responses.append((0x3b61,self.contents()))
        return responses, dict(action='parcel_duplicate_pickup' if event['action']=='duplicate_pickup'
                               else 'parcel_pickup',parcel_id=parcel,item_index=index,
                               definition=item.definition,quantity=event.get('quantity',1),
                               remaining=self.remaining[index],reserve=weapon.reserve,
                               experimental=True)


class ParcelCatalogState:
    def __init__(self, fixture):
        self.containers = [ContainerState(x) for x in fixture.containers]

    def register(self, command, body):
        for container in self.containers:
            container.register(command,body)

    def observe_motion(self, body, weapon):
        if len(body) != 73:
            return None
        uid = struct.unpack_from('>Q', body)[0]
        container = next((x for x in self.containers
                          if x.fixture.uid == uid and x.fixture.native_motion), None)
        return container.observe_motion(body, weapon) if container else None

    def handle(self, command, body, weapon):
        if command == 0x656f:
            if len(body) != 8:
                raise ValueError('AIR_DROP_OPEN_REQ ожидает 8 байт')
            uid = struct.unpack('>Q',body)[0]
            candidate = next((x for x in self.containers if x.fixture.uid == uid),None)
        else:
            if len(body) != 33:
                raise ValueError('PICK_REQ ожидает 33 байта')
            index = struct.unpack_from('>I',body)[0]
            candidate = next((x for x in self.containers if x.fixture.index == index),None)
        if candidate:
            return candidate.handle(command,body,weapon)
        return [], dict(action='parcel_unknown_container')


def load_parcel_fixture(path, weapon, catalog=None):
    path = Path(path)
    if path.stat().st_size > 128 * 1024:
        raise ValueError('Описание контейнеров превышает 128 КиБ')
    config = json.loads(path.read_text())
    return ParcelCatalog.load(path,weapon,catalog) if 'parcels' in config else ParcelFixture.load(path)


def make_parcel_state(fixture):
    return ParcelCatalogState(fixture) if isinstance(fixture,ParcelCatalog) else ParcelState(fixture)
