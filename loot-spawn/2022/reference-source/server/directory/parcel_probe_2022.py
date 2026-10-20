"""Одиночный контейнер аирдропа 2022 с экспериментальным содержимым.

6571 связывает модель с parcel_id, 656f запрашивает её содержимое,
первое слово 3b61 адресует interactive component+116 (140d6285a).
Поддержан только один проверяемый предмет: 12ga, definition 30004.
"""
from dataclasses import dataclass
import json
from pathlib import Path
import struct


@dataclass(frozen=True)
class ParcelFixture:
    uid: int
    index: int
    item_index: int
    quantity: int
    position: tuple

    @classmethod
    def load(cls, path):
        path = Path(path)
        config = json.loads(path.read_text())
        payload = (path.parent / config['entity_file']).read_bytes()
        if len(payload) != 117 or struct.unpack_from('>I', payload, 8)[0] != 501:
            raise ValueError('Нужна проверенная модель зимнего аирдропа 654b/501')
        uid = struct.unpack_from('>Q', payload)[0]
        index = config['parcel_id']
        item_index = config['item_index']
        quantity = config['quantity']
        if (not uid or any(type(v) is not int or not 1 <= v <= 0xffffffff
                           for v in (index, item_index))
                or type(quantity) is not int or not 1 <= quantity <= 100):
            raise ValueError('Неверный идентификатор или количество контейнера')
        return cls(uid, index, item_index, quantity,
                   struct.unpack_from('>iii', payload, 20))


class ParcelState:
    def __init__(self, fixture):
        self.fixture = fixture
        self.spawned = False
        self.linked = False
        self.picked = False
        self.opened = False
        self.remaining = fixture.quantity

    def register(self, command, payload):
        if (command == 0x654b and len(payload) == 117
                and struct.unpack_from('>QI', payload) == (self.fixture.uid, 501)):
            self.spawned = True
        elif (command == 0x6571 and len(payload) == 12
              and struct.unpack('>QI', payload) == (self.fixture.uid, self.fixture.index)):
            self.linked = True
        elif (command == 0x654c and len(payload) == 8
              and struct.unpack('>Q',payload)[0] == self.fixture.uid):
            self.spawned = self.linked = False

    def contents(self):
        if self.picked:
            return struct.pack('>III', self.fixture.index, 0, 0)
        # ITEM kind 1: definition, quantity, четыре нулевых слова и Q0.
        item = struct.pack('>8IQ', self.fixture.item_index, 1,
                           30004, self.remaining, 0, 0, 0, 0, 0)
        return struct.pack('>II', self.fixture.index, 1) + item + bytes(4)

    def handle(self, command, payload, weapon):
        if command == 0x656f:
            if len(payload) != 8:
                raise ValueError('AIR_DROP_OPEN_REQ ожидает 8 байт')
            uid = struct.unpack('>Q', payload)[0]
            if uid != self.fixture.uid or not self.spawned or not self.linked:
                return [], {'action': 'parcel_open_rejected', 'uid': hex(uid)}
            self.opened = True
            return [(0x3b61, self.contents())], {'action': 'parcel_open',
                'uid': hex(uid), 'parcel_id': self.fixture.index,
                'quantity': self.remaining}
        if command == 0x3b63:
            if len(payload) != 33:
                raise ValueError('PICK_REQ ожидает 33 байта')
            parcel, index, target, byte, short, flag, x, y, z, tail = struct.unpack('>IIQBHB3iB', payload)
            distance = sum((a-b)**2 for a, b in zip((x,y,z), self.fixture.position))
            if (not self.spawned or not self.linked or not self.opened
                    or index != self.fixture.item_index or parcel != self.fixture.index
                    or target or byte or short or flag != 1 or tail or distance >= 750**2):
                return [], {'action': 'parcel_pick_rejected'}
            duplicate = self.picked
            amount = 0
            if not duplicate:
                amount = min(self.remaining, weapon.ammunition_room(30004))
                weapon.reserve += amount
                self.remaining -= amount
                self.picked = self.remaining == 0
            # Ground PICK использует индекс сущности и slot 0; контейнерный
            # запрос в dione-parcel-auto: parcel 15520, item 15521.
            # Пара и выдача 20 патронов подтверждены в dione-integrated-01.
            ack = struct.pack('>IIIBI', parcel, index, amount, 1, 30004) + bytes(28)
            replies = [(0x3b64,ack), (0x5fb,weapon.inventory()),
                       (0x3b61,self.contents()), weapon.capacity_sync()]
            replies.extend(weapon.magazine_syncs())
            return replies, {
                'action': 'parcel_duplicate_pickup' if duplicate else 'parcel_pickup',
                'parcel_id': parcel, 'item_index': index,
                'quantity': amount, 'remaining': self.remaining, 'reserve': weapon.reserve,
                'experimental': True}
        return [], {'action': 'parcel_ignored', 'command': hex(command)}
