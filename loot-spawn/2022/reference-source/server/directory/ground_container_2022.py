"""Стационарный учебный запас: ground821/subtype1, без501/полёта/баллона.

Использует проверенный wire выпавшего инвентаря. Размещение и2000патронов
каждого калибра — настройки нашего тира, не исходный ресурсный пресет.
"""
from dataclasses import dataclass
import json
import math
from pathlib import Path
import struct

from death_parcel_2022 import DeathParcelState
from parcel_catalog_2022 import ContainerFixture, ContainerState
from weapon_probe_2022 import AMMUNITION_WEIGHTS, LootFixture


@dataclass(frozen=True)
class GroundContainerFixture:
    container: ContainerFixture
    entity: bytes

    @classmethod
    def load(cls, path, weapon, catalog=None):
        path = Path(path)
        if path.stat().st_size > 16384:
            raise ValueError('Описание запаса превышает16КиБ')
        config = json.loads(path.read_text())
        if set(config) != {'map_id','uid','index','position','ammunition'} or config['map_id'] != 16010:
            raise ValueError('Нужен явный запас зимнего тира16010')
        uid, index, position = int(str(config['uid']),0), config['index'], config['position']
        if (not 0 < uid < 2**64 or type(index) is not int or not 470000 <= index <= 479000
                or not isinstance(position,list) or len(position) != 3
                or any(type(v) not in (int,float) or not math.isfinite(v) or abs(v)>10000000 for v in position)):
            raise ValueError('Неверные UID/index/позиция запаса')
        position = tuple(map(round,position))
        if not weapon or not weapon.all_loot:
            raise ValueError('Запас требует проверенный ground821 шаблон')
        template = weapon.all_loot[0].entity
        if len(template) != 100 or template[62] != 2 or struct.unpack_from('>I',template)[0] != 30201002:
            raise ValueError('Нужен ground821/subtype2,100байт')
        known = tuple(weapon.all_loot) + (catalog.items if catalog else ())
        indexes = {x.index for x in known};uids = {x.entity_uid for x in known}
        if index in indexes or uid in uids:
            raise ValueError('Запас пересекается с лутом сцены')
        ammunition = config['ammunition']
        if not isinstance(ammunition,list) or not 1 <= len(ammunition) <= 7:
            raise ValueError('Нужны1..7 типов патронов')
        seen,items = set(),[]
        for row in ammunition:
            if not isinstance(row,dict) or set(row) != {'definition','quantity'}:
                raise ValueError('Патроны требуют definition/quantity')
            definition, quantity = row['definition'],row['quantity']
            if (type(definition) is not int or definition not in AMMUNITION_WEIGHTS or definition in seen
                    or type(quantity) is not int or not 1 <= quantity <= 2000):
                raise ValueError('Неизвестный/повторный калибр либо количество вне1..2000')
            seen.add(definition)
            # Существующий учёт ограничивает одну пачку999. Не повышаем лимит
            # общего инвентаря ради стенда:2000 =999+999+2 в контейнере.
            while quantity:
                count = min(quantity,999);quantity -= count
                item_index = index+len(items)+1
                item_uid = 0x31d0600000000+item_index
                if item_index in indexes or item_uid in uids or item_uid == uid:
                    raise ValueError('Предмет запаса пересекается с лутом сцены')
                body = bytearray(template)
                struct.pack_into('>Q',body,4,item_uid)
                struct.pack_into('>3i',body,29,*position)
                struct.pack_into('>III',body,63,definition,count,item_index)
                ack = struct.pack('>IIIBI',item_index,0,count,1,definition)+bytes(28)
                items.append(LootFixture(item_uid,item_index,count,position,ack,definition,bytes(body)))
        body = bytearray(template)
        struct.pack_into('>Q',body,4,uid)
        struct.pack_into('>3i',body,29,*position)
        body[62] = 1
        struct.pack_into('>III',body,63,0,0,index)
        return cls(ContainerFixture(uid,index,position,tuple(items)),bytes(body))


class GroundContainerState(DeathParcelState):
    def __init__(self, fixture):
        super().__init__()
        self.fixture = fixture
        container = ContainerState(fixture.container)
        container.spawned = container.linked = True
        self.containers.append(container)

    def snapshot(self):
        return [(0x821,self.fixture.entity),*self.reconcile()]

    def transfer(self, *args, **kwargs):
        raise ValueError('Стационарный запас не принимает инвентари погибших')
