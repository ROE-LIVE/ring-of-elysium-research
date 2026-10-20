"""Собственная выдача лута по близости к игроку; исходный AOI ROE не восстановлен.

Каталог содержит только поддержанные предметы и координаты. Клиент получает
обычные 821/82b, а pickup обслуживает существующий WeaponState.
"""
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import struct

from weapon_probe_2022 import AMMUNITION_WEIGHTS, ARMOR_DURABILITY, EQUIPMENT_SLOTS, GUN_PROFILES, MEDICAL_PROFILES, SUPPORTED_ATTACHMENTS, LootFixture
from throwable_inventory_2022 import THROWABLE_PROFILES


def record_catalog_summary(run, path, catalog):
    """Описание уже проверенного снимка, без исходного пути или содержимого JSON."""
    summary_path = Path(run) / 'launch-summary.json'
    if not summary_path.is_file():
        return
    summary = json.loads(summary_path.read_text(encoding='utf-8-sig'))
    summary.update(loot_catalog_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                   loot_catalog_items=len(catalog.items), loot_catalog_radius_cm=catalog.radius,
                   loot_catalog_bounds_cm=[min(item.position[axis] for item in catalog.items)
                                           for axis in range(3)] +
                                          [max(item.position[axis] for item in catalog.items)
                                           for axis in range(3)])
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


@dataclass(frozen=True)
class LootCatalog:
    items: tuple
    radius: int
    visible_limit: int
    batch_limit: int

    @classmethod
    def load(cls, path, template):
        path = Path(path)
        if path.stat().st_size > 16 * 1024 * 1024:
            raise ValueError('Каталог превышает 16 МиБ')
        config = json.loads(path.read_text(encoding='utf-8-sig'))
        if len(template) != 100:
            raise ValueError('Нужен проверенный шаблон ground821')
        radius = config.get('radius_cm', 2000)
        visible = config.get('visible_limit', 128)
        batch = config.get('batch_limit', 16)
        if (type(radius) is not int or not 100 <= radius <= 10000
                or type(visible) is not int or not 1 <= visible <= 256
                or type(batch) is not int or not 1 <= batch <= 32):
            raise ValueError('Неверные пределы видимости лута')
        rows = config.get('entities')
        if not isinstance(rows, list) or not 1 <= len(rows) <= 50000:
            raise ValueError('Нужно 1..50000 предметов каталога')
        items, indexes, uids = [], set(), set()
        for row in rows:
            index, uid = row['index'], row['entity_uid']
            definition, quantity = row['item_id'], row['quantity']
            position = row['position']
            durability = row.get('durability')
            if (type(index) is not int or not 1 <= index <= 0xffffffff
                    or type(uid) is not int or not 1 <= uid <= 0xffffffffffffffff
                    or index in indexes or uid in uids
                    or type(definition) is not int
                    or definition not in (*AMMUNITION_WEIGHTS, *GUN_PROFILES, *EQUIPMENT_SLOTS, *MEDICAL_PROFILES, *SUPPORTED_ATTACHMENTS, *THROWABLE_PROFILES)
                    or type(quantity) is not int or not 1 <= quantity <= 100
                    or (definition not in (*AMMUNITION_WEIGHTS, *MEDICAL_PROFILES, *THROWABLE_PROFILES) and quantity != 1)
                    or not isinstance(position, list) or len(position) != 3
                    or any(type(n) is not int or abs(n) > 10000000 for n in position)):
                raise ValueError('Неверный или повторный предмет каталога')
            if durability is not None and (definition not in ARMOR_DURABILITY
                    or type(durability) is not int
                    or not 0 <= durability <= ARMOR_DURABILITY[definition]):
                raise ValueError('Прочность допустима только в пределах выбранной брони')
            body = bytearray(template)
            struct.pack_into('>Q', body, 4, uid)
            struct.pack_into('>3i', body, 29, *position)
            struct.pack_into('>III', body, 63, definition, quantity, index)
            ack = struct.pack('>IIIBI', index, 0, quantity, 1, definition) + bytes(28)
            items.append(LootFixture(uid, index, quantity, tuple(position), ack,
                                     definition, bytes(body), durability=durability))
            indexes.add(index)
            uids.add(uid)
        return cls(tuple(items), radius, visible, batch)

    def validate_fixture(self, fixture):
        if ({x.index for x in self.items} & {x.index for x in fixture.all_loot}
                or {x.entity_uid for x in self.items} & {x.entity_uid for x in fixture.all_loot}):
            raise ValueError('Каталог пересекается с фиксированным лутом')


class LootCatalogState:
    def __init__(self, catalog, weapon):
        catalog.validate_fixture(weapon.fixture)
        self.catalog, self.weapon = catalog, weapon
        self.visible = set()
        self.initial_position_reported = False
        self.buckets = {}
        for item in catalog.items:
            if item.index in weapon.loot_registry:
                raise ValueError('Повторный индекс в состоянии оружия')
            weapon.loot_registry[item.index] = item
            key = tuple(n // catalog.radius for n in item.position[:2])
            self.buckets.setdefault(key, []).append(item.index)

    def poll(self):
        position = self.weapon.position
        if position is None:
            return [], []
        radius = self.catalog.radius
        bx, by = (n // radius for n in position[:2])
        candidates = []
        for x in range(bx - 1, bx + 2):
            for y in range(by - 1, by + 2):
                for index in self.buckets.get((x, y), []):
                    if index in self.weapon.picked_loot:
                        continue
                    item = self.weapon.loot_registry[index]
                    distance = sum((a - b) ** 2 for a, b in zip(item.position, position))
                    if distance <= radius * radius:
                        candidates.append((distance, index))
        desired = {index for _, index in sorted(candidates)[:self.catalog.visible_limit]}
        remove = sorted(self.visible - desired)[:self.catalog.batch_limit]
        add = sorted(desired - self.visible)[:self.catalog.batch_limit - len(remove)]
        packets = []
        for index in remove:
            item = self.weapon.loot_registry[index]
            # WeaponState уже отправил 82b после полного pickup.
            if index not in self.weapon.picked_loot:
                packets.append((0x82b, struct.pack('>Q', item.entity_uid)))
            # Подобранный UID тоже недоступен; повтор распознаётся picked_loot,
            # а не ошибочным остатком в available_loot после удаления из AOI.
            self.weapon.available_loot.discard(item.entity_uid)
            self.visible.remove(index)
        for index in add:
            item = self.weapon.loot_registry[index]
            packets.append((0x821, item.entity))
            self.weapon.available_loot.add(item.entity_uid)
            self.visible.add(index)
        events = []
        if remove or add or not self.initial_position_reported:
            events.append(dict(action='catalog_visibility', spawned=len(add),
                               removed=len(remove), visible=len(self.visible),
                               spawned_indexes=add, removed_indexes=remove,
                               catalog_total=len(self.catalog.items),
                               position=list(position),
                               original_aoi_verified=False))
            self.initial_position_reported = True
        return packets, events
