"""Публичные XML: комментарии, обе формы процентов и границы H1."""
from pathlib import Path
import random
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from export_loot_tables_2022 import read_table, count_distribution, extra_bundle, simulate


class LootTableTests(unittest.TestCase):
    def test_comments_declared_count_and_versions_do_not_create_rows(self):
        source = '''<NewObj ObjName="fixture"><items ArrayCount="1" [XlsProp]="1">
<!--<item iID="9" iMapID="16010"/>-->
<item iID="51" iMapID="16010" vNumPercent="17;25"><vNumPercentArray>
<vNumPercentArray v="17"/><vNumPercentArray v="29"/></vNumPercentArray></item>
<item iID="51" iMapID="16005" vNumPercent="100"/>
<item iID="3" iMapID="16010" vNumPercent="20;23"/>
</items></NewObj>'''
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)/'table.xml'
            path.write_text(source)
            rows = read_table(path, 16010)['rows']
        self.assertEqual([row['iID'] for row in rows], ['51', '3'])
        self.assertEqual(rows[0]['source_line'], 3)
        self.assertEqual(count_distribution(rows[0], 'scalar'), [58, 17, 25])
        self.assertEqual(count_distribution(rows[0], 'array'), [54, 17, 29])

    def test_zero_weight_item_never_selected_and_guaranteed_count(self):
        control = {'num_percent_array': [100]}
        items = [{'iItemID': '10402', 'iCount': '1'}, {'iItemID': '99999', 'iCount': '0'}]
        sample = simulate(control, items, 25, 17, 'array')
        self.assertEqual(sample['occupancy'], {1: 25})
        self.assertEqual(sample['selected_items'], {'10402': 25})
        self.assertFalse(sample['original_algorithm_verified'])
        self.assertEqual(sample, simulate(control, items, 25, 17, 'array'))

    def test_extra_stacks_and_missing_distribution(self):
        row = dict(iExtraItemID1='30004', iExtraItemCount1='2',
                   iExtraItemStackCount1='10', iExtraItemWeight1='100')
        self.assertEqual(extra_bundle(row, random.Random(1)),
                         [dict(item_id=30004, quantity=10)]*2)
        for control in ({'num_percent_array': [101]}, {'num_percent_array': []}):
            with self.assertRaises(ValueError):
                count_distribution(control, 'array')
        with self.assertRaises(ValueError):
            simulate({'num_percent_array': [100]}, [], 1, 1, 'array')


if __name__ == '__main__':
    unittest.main()
