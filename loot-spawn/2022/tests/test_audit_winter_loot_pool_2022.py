"""Публичные определения: адресная нормализация и сохранение источника."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from audit_winter_loot_pool_2022 import definitions


class DefinitionTests(unittest.TestCase):
    def test_adjacent_attributes_are_normalized_without_changing_source_or_lines(self):
        raw = (b'<NewObj ObjName="Public">\n<mItems [XlsProp]="1">\n'
               b'<mItems dwStringID="70001" szName="Bandage"nWeight="2"/>\n'
               b'</mItems></NewObj>')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'items.xml'
            path.write_bytes(raw)
            rows, source = definitions(path)
            self.assertEqual(path.read_bytes(), raw)
        self.assertEqual(rows[70001][0]['attributes']['nWeight'], '2')
        self.assertEqual(rows[70001][0]['source_lines'], [3])
        self.assertEqual(source['adjacent_attribute_separators'], 1)
        self.assertEqual(source['sha256'], hashlib.sha256(raw).hexdigest())

    def test_duplicate_definitions_remain_ambiguous_instead_of_last_write_wins(self):
        raw = ('<NewObj>\n<mItems dwStringID="42" szName="First"/>\n'
               '<mItems dwStringID="42" szName="Second"/>\n</NewObj>')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'items.xml'
            path.write_text(raw)
            rows, _ = definitions(path)
        self.assertEqual(len(rows[42]), 2)
        self.assertEqual(rows[42][0]['source_lines'], [2, 3])
