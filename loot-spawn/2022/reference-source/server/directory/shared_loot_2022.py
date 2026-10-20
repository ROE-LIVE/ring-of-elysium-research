"""Общий наземный лут и эпоха диагностической комнаты2022.

Обработка запроса и фиксация остатка синхронны в одном event loop endpoint.
Диагностическая эпоха сбрасывается после удаления последнего участника комнаты.
"""
import struct
from death_parcel_2022 import DeathParcelState


class SharedLootRooms:
    def __init__(self, fixture, share_death_parcels=False):
        self.fixture = fixture
        self.share_death_parcels = share_death_parcels
        self.rooms = {}
        self.drop_counter = 0
        self.instance_counter = 0
        self.epochs = {}

    def room(self, state):
        uid = state['room_uid']
        if not 0 < uid < 2**64:
            raise ValueError('Нужен UID комнаты общего лута')
        if uid not in self.epochs and len(self.epochs) >= 32:
            raise ValueError('Лимит диагностических UID комнат')
        epoch = self.epochs.setdefault(uid, 1)
        if state.get('shared_loot_epoch', epoch) != epoch:
            raise ValueError('Истёкшая эпоха общего лута')
        state['shared_loot_epoch'] = epoch
        if uid not in self.rooms:
            if len(self.rooms) >= 32:
                raise ValueError('Лимит диагностических комнат')
            items = {item.index: item for item in self.fixture.all_loot}
            self.rooms[uid] = dict(items=items, consumed=set(), active=set(), members={})
        return self.rooms[uid]

    def allocate_instance(self):
        self.instance_counter += 1
        if self.instance_counter > 65536:
            raise ValueError('Лимит общих instance UID')
        return 0x1e01000000000000 + self.instance_counter

    def allocate_ground(self):
        self.drop_counter += 1
        if self.drop_counter > 8192:
            raise ValueError('Лимит общего наземного лута')
        index = 0x10000000 + self.drop_counter
        uid = 0x31d0003000000 + self.drop_counter
        return index, uid

    def world_start(self, state, now):
        """Общий календарь текущей эпохи, доступный только её участнику."""
        room = self.room(state)
        if room['members'].get(state['actor_uid']) is not state:
            raise ValueError('Календарь требует участника комнаты')
        return room.setdefault('world_started', now)

    def attach(self, state):
        room = self.room(state)
        account = state['actor_uid']
        old = room['members'].get(account)
        if old is not None and old is not state and not state.get('gameplay_resumed'):
            return False
        if old is None and len(room['members']) >= 8:
            return False
        room['members'][account] = state
        if self.share_death_parcels:
            state['death_parcels'] = room.setdefault('death_parcels',DeathParcelState(shared=True))
        weapon = state.get('weapon')
        if weapon:
            if weapon.instance_allocator is None:
                weapon.instance_allocator = self.allocate_instance
                for gun in weapon.guns.values():
                    gun.uid = self.allocate_instance()
            weapon.ground_allocator = self.allocate_ground
            for index, item in room['items'].items():
                weapon.loot_registry[index] = item
                if index in room['consumed'] or index not in room['active']:
                    weapon.available_loot.discard(item.entity_uid)
                else:
                    weapon.available_loot.add(item.entity_uid)
            primary = weapon.fixture.loot
            weapon.loot_available = bool(primary and primary.index in room['active']
                                         and primary.index not in room['consumed'])
        return True

    def filter_spawn(self, state, payload):
        """Не возвращать подобранное при повторном821/позднем входе."""
        if len(payload) != 100:
            return payload
        uid = struct.unpack_from('>Q', payload, 4)[0]
        room = self.room(state)
        for index, item in room['items'].items():
            if item.entity_uid == uid:
                room['active'].add(index)
                return None if index in room['consumed'] else item.entity
        return payload

    def snapshot(self, state):
        """Текущая земля позднего входа/RELAY, без повторного зачисления вещей."""
        room = self.room(state)
        if room['members'].get(state['actor_uid']) is not state:
            return []
        messages = [(0x82b, struct.pack('>Q', room['items'][index].entity_uid))
                    for index in sorted(room['consumed'])]
        # Начальные821 уже выдаёт scene-rule с фильтром актуального остатка.
        initial = {item.index for item in self.fixture.all_loot}
        messages.extend((0x821, room['items'][index].entity)
                        for index in sorted(room['active'] - room['consumed'] - initial))
        if self.share_death_parcels:
            messages.extend((0x821,body) for body in room['death_parcels'].spawns)
        return messages

    def publish_external_drops(self, state, packets):
        room = self.room(state)
        updates = []
        for code,body in packets:
            if code != 0x821 or len(body) != 100 or body[62] != 2:
                continue
            index = struct.unpack_from('>I',body,71)[0]
            item = state['weapon'].loot_registry.get(index)
            if item and index not in room['items']:
                room['items'][index] = item
                room['active'].add(index)
                updates.append((code,body))
        return [(other,updates) for other in room['members'].values()
                if other is not state and updates]

    def death_outputs(self, state, packets, contents=False):
        room = self.room(state)
        corpses = room.get('death_parcels')
        if not corpses:
            return []
        return [(other,[(code,body) for code,body in packets
                        if code == 0x821 or (contents and code == 0x3b61
                        and other['actor_uid'] in corpses.openers.get(struct.unpack_from('>I',body)[0],set()))])
                for other in room['members'].values() if other is not state]

    def detach(self, state):
        uid = state.get('room_uid')
        room = self.rooms.get(uid)
        if room is None or room['members'].get(state.get('actor_uid')) is not state:
            return False
        del room['members'][state['actor_uid']]
        if room['members']:
            return False
        del self.rooms[uid]
        self.epochs[uid] = self.epochs.get(uid, 1) + 1
        return True

    def handle(self, state, command, payload):
        weapon = state['weapon']
        if not self.attach(state):
            return [], dict(action='rejected', reason='shared_loot_duplicate_or_limit'), []
        room = self.room(state)
        pickup = command == 0x3b63 and len(payload) == 33
        index = struct.unpack_from('>I', payload)[0] if pickup else None
        item = room['items'].get(index)
        if item is not None and index in room['consumed']:
            responses = [(0x82b, struct.pack('>Q', item.entity_uid))]
            responses.extend(weapon.reconcile_inventory())
            return responses, dict(action='rejected', reason='shared_loot_consumed', index=index), []
        responses, event = weapon.handle(command, payload)
        updates = []
        if item is not None and event.get('action') == 'pickup' and event.get('quantity', 0) > 0:
            updates.append((0x82b, struct.pack('>Q', item.entity_uid)))
            if event['remaining']:
                room['items'][index] = weapon.loot_registry[index]
                updates.append((0x821, room['items'][index].entity))
            else:
                room['consumed'].add(index)
        # Выброшенные предметы и замена занятого слота получают общий index/UID.
        for code, body in responses:
            if code != 0x821 or len(body) != 100:
                continue
            dropped_index = struct.unpack_from('>I', body, 71)[0]
            dropped = weapon.loot_registry.get(dropped_index)
            if dropped_index not in room['items'] and dropped is not None:
                room['items'][dropped_index] = dropped
                room['active'].add(dropped_index)
                updates.append((code, body))
        outputs = [(other, updates) for other in room['members'].values()
                   if other is not state and updates and not other.get('match_finished')
                   and not other.get('transport_retired')]
        if updates:
            event = dict(event, shared_ground=True, shared_recipients=len(outputs))
        return responses, event, outputs
