"""Регрессии источников карты и выбора тестового участка лута2022."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from recover_winter_loot_presets_2022 import read_points
import generate_winter_loot_catalog_2022 as catalog


class LootPresetTests(unittest.TestCase):
    def test_point_source_preserves_signed_height_and_line(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'points.xml'
            source.write_text('<Root>\n<PointCfg InstanceID="17" TypeId="3" PosX="1" '
                              'PosY="2" PosZ="-40" Direction="122"/>\n</Root>')
            result = read_points(source)
            self.assertEqual(result['points'][0]['position_cm'], [1, 2, -40])
            self.assertEqual(result['points'][0]['source_line'], 2)
            source.write_text(source.read_text().replace('</Root>',
                              '<PointCfg InstanceID="17" TypeId="5" PosX="1" '
                              'PosY="2" PosZ="3" Direction="0"/>\n</Root>'))
            with self.assertRaises(ValueError):
                read_points(source)

    def test_region_excludes_other_floors_xy_without_changing_authored_xyz(self):
        points = dict(map_id=16010, source_sha256=catalog.XML_SHA, points=[
            dict(instance_id=n, type_id=3, source_line=n, direction=122,
                 position_cm=pos) for n, pos in enumerate(
                     ([10, 20, -40], [10, 20, 800], [1000, 2000, 3000]), 1)])
        controls = [dict(iID=str(cid), iMapID='16010', iRadius='200', num_percent_array=[100])
                    for cid in (1, 3, 5)]
        tables = dict(control=dict(rows=controls, path='control.xml', sha256='test'),
                      items=dict(rows=[dict(iID='17', iCtrlID='3', iItemID='10402',
                                            iCount='1')], path='items.xml', sha256='test'))
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'points.json'
            source.write_text(json.dumps(points))
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            with patch.object(catalog, 'POINTS_SHA', digest), patch.object(catalog, 'export', return_value=tables):
                result = catalog.build(source, directory, 1, authored_xyz=True,
                                       bounds_cm=[10, 20, 30, 40])
                self.assertEqual([e['position'] for e in result['entities']],
                                 [[10, 20, -40], [10, 20, 800]])
                self.assertFalse(result['original_algorithm_verified'])
                self.assertEqual(result['groups'][0]['source_points'], 0)
                for bounds in ([50, 50, 60, 60], [10, 20, 10, 40], [True, 0, 10, 20]):
                    with self.assertRaises(ValueError):
                        catalog.build(source, directory, 1, bounds_cm=bounds)
            source.write_text(source.read_text()+' ')
            with self.assertRaises(ValueError):
                catalog.build(source, directory, 1)


if __name__ == '__main__':
    unittest.main()
