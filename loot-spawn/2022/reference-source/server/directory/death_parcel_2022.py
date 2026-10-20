"""Выпавший инвентарь: native821/subtype1, BCE, 3b61, 3b63.

Распределение вещей при смерти — явная политика нашего peer. Wire проверен
на клиенте2022; исходные правила исключения предметов пока неизвестны.
"""
from dataclasses import replace
from copy import copy,deepcopy
import struct

from parcel_catalog_2022 import ContainerFixture, ContainerState
from weapon_probe_2022 import (LootFixture, WeaponState, AMMUNITION_WEIGHTS,
                              GUN_PROFILES, EQUIPMENT_SLOTS, MEDICAL_PROFILES,
                              SUPPORTED_ATTACHMENTS, THROWABLE_PROFILES)


def target_inventory(actor, weapon_fixture):
    """Отдельный живой учёт пассивной мишени, без копирования вещей игрока."""
    fixture = actor.fixture
    if fixture.death_loot_reserve is None:
        return None
    equipment = tuple(d for d in (fixture.armor_definition, fixture.helmet_definition) if d)
    state = WeaponState(replace(weapon_fixture, gun_on_start=bool(fixture.equipment),
                               reserve=fixture.death_loot_reserve,
                               starting_equipment=equipment, starter_items=(),
                               winter_starter_inventory=False,
                               cosmetics_config_file=None), fixture.uid)
    if fixture.equipment:
        # EQUIP_CHANGE_TOALL: actorQ/countI, definitionI/instanceQ.
        state.guns[1].uid = struct.unpack_from('>Q', fixture.equipment, 16)[0]
    if fixture.armor_definition:
        state.equipment_durability[12] = actor.armor_durability
    if fixture.helmet_definition:
        state.equipment_durability[10] = actor.helmet_durability
    return state


class DeathParcelState:
    def __init__(self, shared=False):
        self.containers = []
        self.owners = set()
        self.shared = shared
        self.openers = {}
        self.spawns = []

    def transfer(self, owner, position, reserved_indexes=()):
        """Сначала построить весь пакет, затем однократно очистить источник."""
        if owner.actor_uid in self.owners:
            return [], {'action': 'death_inventory_duplicate', 'owner': hex(owner.actor_uid)}
        template = owner.ground_template
        if (template is None or len(template) != 100 or template[62] != 2
                or struct.unpack_from('>I', template)[0] != 30201002):
            raise ValueError('Смерть требует проверенный ground821/subtype2')
        position = tuple(round(x) for x in position)
        if len(position) != 3 or any(not -2**31 <= x < 2**31 for x in position):
            raise ValueError('Неверная позиция выпавшего пакета')
        sequence = len(self.containers) + 1
        if sequence > 16:
            raise ValueError('Превышен предел16 пакетов смерти')
        parcel_id = 450000 + sequence * 100
        uid = 0x31d040000f0000 + sequence
        records = []
        for gun in owner.guns.values():
            records.append((gun.definition, 1, gun.clip, None, gun.uid, tuple(gun.parts.items()), gun.skin_id))
        for definition in (30004, *owner.extra_ammunition):
            quantity = owner.ammunition_quantity(definition)
            if quantity:
                records.append((definition, quantity, None, None, None, (), None))
        for slot, definition in owner.equipment.items():
            # Зимний набор остаётся способностью: правило оригинального сервера
            # неизвестно. Броня и шлем передаются с текущей прочностью, включая0.
            if slot in (10, 12):
                records.append((definition, 1, None, owner.equipment_durability[slot], None, (), None))
        for definition, quantity in (*owner.medical.items(), *owner.throwables.items(),
                                     *owner.equipped_throwables.values()):
            records.append((definition, quantity, None, None, None, (), None))
        for item in owner.attachments.values():
            records.append((item.definition, 1, None, None, item.uid, (), None))
        if len(records) > 90:
            raise ValueError('Слишком много предметов в пакете смерти')
        reserved = set(reserved_indexes) | set(owner.loot_registry)
        if any(parcel_id+n in reserved for n in range(len(records)+1)):
            raise ValueError('Индексы пакета смерти заняты текущим лутом')
        items = []
        for n, (definition, quantity, clip, durability, instance_uid, parts, skin_id) in enumerate(records, 1):
            supported = (AMMUNITION_WEIGHTS.keys() | GUN_PROFILES.keys()
                         | EQUIPMENT_SLOTS.keys() | MEDICAL_PROFILES.keys()
                         | SUPPORTED_ATTACHMENTS | THROWABLE_PROFILES.keys())
            if definition not in supported or type(quantity) is not int or not 1 <= quantity <= 999:
                raise ValueError('Неподдержанный предмет в живом инвентаре')
            index = parcel_id + n
            body = bytearray(template)
            item_uid = 0x31d0500000000 + index
            struct.pack_into('>Q', body, 4, item_uid)
            struct.pack_into('>3i', body, 29, *position)
            struct.pack_into('>III', body, 63, definition, quantity, index)
            ack = struct.pack('>IIIBI', index, 0, quantity, 1, definition) + bytes(28)
            items.append(LootFixture(item_uid, index, quantity, position, ack,
                                     definition, bytes(body), clip, durability, instance_uid, parts, skin_id))
        container = ContainerState(ContainerFixture(uid, parcel_id, position, tuple(items)))
        body = bytearray(template)
        struct.pack_into('>Q', body, 4, uid)
        struct.pack_into('>3i', body, 29, *position)
        body[62] = 1
        struct.pack_into('>III', body, 63, 0, 0, parcel_id)
        # Commit после полной проверки/кодирования: источник больше не владеет
        # вещами. История ground pickup остаётся для защиты от повторной выдачи.
        owner.guns.clear()
        owner.reserve = 0
        owner.extra_ammunition.clear()
        owner.medical.clear()
        owner.throwables.clear()
        owner.equipped_throwables.clear()
        owner.attachments.clear()
        for slot in (10, 12):
            owner.equipment.pop(slot, None)
            owner.equipment_durability.pop(slot, None)
        owner.pending_reload = None
        owner.hand_slot = 0
        container.spawned = container.linked = True
        self.containers.append(container)
        self.spawns.append(bytes(body))
        self.owners.add(owner.actor_uid)
        return [(0x821, bytes(body))], {
            'action': 'death_inventory_transferred', 'owner': hex(owner.actor_uid),
            'uid': hex(uid), 'parcel_id': parcel_id,
            'items': [dict(index=x.index, definition=x.definition, quantity=x.quantity,
                           clip=x.clip, durability=x.durability,
                           instance_uid=hex(x.instance_uid) if x.instance_uid else None,
                           parts=[dict(slot=slot, definition=part.definition,
                                       instance_uid=hex(part.uid)) for slot,part in x.parts]) for x in items],
            'position': position, 'experimental': True}

    def matches(self, command, body):
        if command == 0xbce and len(body) == 16:
            uid = struct.unpack_from('>Q', body)[0]
            return any(x.fixture.uid == uid for x in self.containers)
        if command == 0x3b63 and len(body) == 33:
            index = struct.unpack_from('>I', body)[0]
            return any(x.fixture.index == index for x in self.containers)
        return False

    def reconcile(self, account=None):
        """После handoff возвращаем остаток открытых пакетов, без новых вещей."""
        return [(0x3b61, x.contents()) for x in self.containers if x.opened
                and (not self.shared or account in self.openers.get(x.fixture.index,set()))]

    def handle(self, command, body, weapon):
        if command == 0xbce:
            uid, requester = struct.unpack('>QQ', body)
            container = next(x for x in self.containers if x.fixture.uid == uid)
            position = weapon.position
            if (requester != weapon.actor_uid or position is None
                    or sum((a-b)**2 for a,b in zip(position, container.fixture.position)) >= 750**2):
                return [], {'action': 'death_parcel_open_rejected', 'parcel_id': container.fixture.index}
            container.opened = True
            self.openers.setdefault(container.fixture.index,set()).add(weapon.actor_uid)
            return [(0x3b61, container.contents())], {
                'action': 'death_parcel_open', 'parcel_id': container.fixture.index,
                'remaining': sum(container.remaining.values())}
        index = struct.unpack_from('>I', body)[0]
        container = next(x for x in self.containers if x.fixture.index == index)
        if self.shared:
            if (weapon.actor_uid not in self.openers.get(index,set()) or weapon.position is None
                    or sum((a-b)**2 for a,b in zip(weapon.position,container.position)) >= 750**2):
                return [],dict(action='death_parcel_pick_rejected',reason='not_open_or_near',parcel_id=index)
            item_index = struct.unpack_from('>I',body,4)[0]
            if not container.remaining.get(item_index,0):
                return [(0x3b61,container.contents())],dict(action='death_parcel_pick_rejected',reason='consumed',parcel_id=index)
            staged = copy(weapon)
            for key,value in weapon.__dict__.items():
                if key not in ('fixture','ground_allocator','instance_allocator'):
                    setattr(staged,key,deepcopy(value))
            staged_container = copy(container)
            staged_container.remaining = dict(container.remaining)
            # registered у singleton относился к одному WeaponState. Для общей
            # комнаты каждому получателю ставим актуальный остаток отдельно.
            staged_container.registered = True
            for item in container.fixture.items:
                quantity = container.remaining[item.index]
                staged.loot_registry[item.index] = replace(container.at_position(item),quantity=quantity)
                if quantity:staged.available_loot.add(item.entity_uid)
                else:staged.available_loot.discard(item.entity_uid)
            packets,event = staged_container.handle(command,body,staged)
            if event.get('action') == 'parcel_pickup' and event.get('quantity',0) > 0:
                weapon.__dict__.update(staged.__dict__)
                container.remaining.update(staged_container.remaining)
            return packets,event
        # ContainerState уже проверяет открытие, форму, расстояние и capacity;
        # виртуальные предметы не создают ground821 при частичном pickup.
        return container.handle(command, body, weapon)
