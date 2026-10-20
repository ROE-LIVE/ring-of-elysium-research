"""Отдельный воспроизводимый план каждого одиночного Training.

При handoff объект плана переносится вместе с состоянием. Следующий вход
в комнату создаёт новый план; явный seed намеренно повторяет сценарий.
"""
import json
from pathlib import Path
import secrets

from seeded_match_2022 import plan_match
from region_index_2022 import FastRegionIndex
from world_probe_2022 import WorldFixture


class SeededScenarioFactory:
    def __init__(self, configuration, output, compile_rules, weapon_fixture=None, parcel_fixture=None):
        path = Path(configuration).resolve()
        if path.stat().st_size > 65536:
            raise ValueError('Настройки сценария превышают64КиБ')
        config = json.loads(path.read_text())
        self.seed = config.get('seed')
        if self.seed is not None and (type(self.seed) is not int or not 0 <= self.seed < 2**63):
            raise ValueError('Replay seed требует uint63')
        self.flight = config.get('native_flight', False)
        if type(self.flight) is not bool:
            raise ValueError('native_flight требует bool')
        self.refuge = config.get('refuge_name')
        self.randomize_drop=config.get('randomize_airdrop',False)
        self.parcel_fixture=parcel_fixture
        if type(self.randomize_drop)is not bool:raise ValueError('randomize_airdrop требует bool')
        if self.randomize_drop:
            from parcel_catalog_2022 import ParcelCatalog
            if (not isinstance(parcel_fixture,ParcelCatalog)or len(parcel_fixture.containers)!=1
                    or not parcel_fixture.containers[0].native_motion):
                raise ValueError('Случайный drop требует одиночный native501 каталог')
        self.world_path = (path.parent/config['world_file']).resolve()
        self.scene_path = (path.parent/config['scene_file']).resolve()
        self.world = json.loads(self.world_path.read_text())
        self.scene = json.loads(self.scene_path.read_text())
        # Относительные wire-ссылки принадлежат шаблону, а не match-0001.
        for rule in self.scene:
            for response in rule['responses']:
                if 'payload_file' in response:
                    response['payload_file'] = str((self.scene_path.parent/response['payload_file']).resolve())
        region_file = self.world['region_grid']['file']
        region_path = (self.world_path.parent/region_file).resolve()
        self.world['region_grid']['file'] = str(region_path)
        self.index = FastRegionIndex.load(region_path)
        self.loot_source = None
        self.weapon_fixture = weapon_fixture
        if config.get('loot_source'):
            if not weapon_fixture or not weapon_fixture.all_loot:
                raise ValueError('SourceLoot требует проверенный ground821 шаблон')
            from extract_prefab_loot_2022 import load_source
            specification=config['loot_source']
            self.loot_source=load_source((path.parent/specification['client']).resolve(),
                (path.parent/specification['manifest']).resolve(),
                (path.parent/specification['cache']).resolve())
        self.output, self.compile_rules, self.ordinal = Path(output), compile_rules, 0
        # Проверяем шаблон до первого входа; не создаём состояние игрока.
        self._generate(self.seed if self.seed is not None else 0)

    def _generate(self, seed):
        world, scene, metadata = plan_match(self.world, self.scene, self.index, seed,
                                           refuge_name=self.refuge)
        if self.randomize_drop:
            from seeded_airdrop_2022 import randomize_airdrop
            from winter_selection_2022 import load_spawn_points
            scene,drop=randomize_airdrop(world,scene,self.index,seed,load_spawn_points())
            metadata.update(drop)
        if self.flight:
            from evacuation_flight_2022 import native_evacuation_scene
            scene = native_evacuation_scene(scene)
        return world, scene, metadata

    def __call__(self):
        seed = self.seed if self.seed is not None else secrets.randbits(63)
        world, scene, metadata = self._generate(seed)
        ordinal = self.ordinal + 1
        metadata['match_ordinal'] = ordinal
        # Последний timer — реальный предел нового локального сценария,
        # а не прежние диагностические2400с независимо от CycleScale.
        last = world['stages'][-1]
        metadata['match_end_seconds'] = last['at_seconds'] + last['duration']
        directory = self.output/('match-%04d' % ordinal)
        directory.mkdir(parents=True, exist_ok=False)
        for name, value in (('world.json',world),('scene.json',scene),('plan.json',metadata)):
            (directory/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        fixture = WorldFixture.load(directory/'world.json')
        rules = self.compile_rules(directory/'scene.json')
        loot_catalog = None
        if self.loot_source:
            from generate_prefab_loot_catalog_2022 import build
            from loot_catalog_2022 import LootCatalog
            nodes,tables,summary=self.loot_source
            catalog=build(nodes,tables,seed)
            catalog.update(source_manifest_sha256=summary['manifest_sha256'])
            catalog_path=directory/'loot-catalog.json'
            catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n')
            loot_catalog=LootCatalog.load(catalog_path,self.weapon_fixture.all_loot[0].entity)
            loot_catalog.validate_fixture(self.weapon_fixture)
            metadata.update(loot_items=len(catalog['entities']),loot_points=len(nodes),
                            loot_policy=catalog['policy'],loot_source_sha256=summary['manifest_sha256'])
            (directory/'plan.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
        self.ordinal = ordinal
        result=dict(match_world_fixture=fixture, match_scene_rules=rules, match_plan=metadata,
                    match_end_seconds=metadata['match_end_seconds'])
        if loot_catalog is not None:result['match_loot_catalog']=loot_catalog
        if self.randomize_drop:
            from dataclasses import replace
            from parcel_catalog_2022 import ParcelCatalog
            import struct
            container=self.parcel_fixture.containers[0]
            if container.uid!=metadata['airdrop_uid']:raise ValueError('UID scene/drop fixture не совпал')
            position=tuple(metadata['airdrop_start_position'])
            items=[]
            for item in container.items:
                body=bytearray(item.entity);struct.pack_into('>3i',body,29,*position)
                items.append(replace(item,position=position,entity=bytes(body)))
            result['match_parcel_fixture']=ParcelCatalog((replace(container,position=position,items=tuple(items)),))
        return result
