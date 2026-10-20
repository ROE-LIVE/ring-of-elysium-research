"""Адресное чтение проверяет диапазон, Zlib EOF и SHA до сохранения XML."""
import hashlib
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from extract_prefab_loot_2022 import read_resource, _relative


class SelectedLootResourcesTests(unittest.TestCase):
    def fixture(self, directory, data=b'<public>42</public>', linked=0):
        packed=zlib.compress(data);blocks=(len(packed)+16+63)//64
        archive=b'vfs '+struct.pack('<II',1,64)+bytes(20)
        archive+=struct.pack('<4sIq',b'data',blocks,linked)+packed
        archive+=bytes(32+blocks*64-len(archive))
        (directory/'test.vfs').write_bytes(archive)
        return dict(path='DATA/test.xml',source='test.vfs',offset=32,
                    storage='vfs_zlib',size=len(data),sha256=hashlib.sha256(data).hexdigest())

    def test_bounded_zlib_resource_and_sha(self):
        with tempfile.TemporaryDirectory()as folder:
            root=Path(folder);record=self.fixture(root)
            self.assertEqual(read_resource(root,record),b'<public>42</public>')
            record['sha256']='0'*64
            with self.assertRaises(ValueError):read_resource(root,record)

    def test_size_bomb_chain_and_unsafe_path_are_rejected(self):
        with tempfile.TemporaryDirectory()as folder:
            root=Path(folder);record=self.fixture(root,b'A'*100000)
            record['size']=10
            with self.assertRaises(ValueError):read_resource(root,record)
            record=self.fixture(root,linked=1000)
            with self.assertRaises(ValueError):read_resource(root,record)
        for name in ('../client','/client','C:/client','x\\client',''):
            with self.assertRaises(ValueError):_relative(name)

    def test_selected_sfc_lz4_uses_expected_usize_and_sha(self):
        from lz4.block import compress
        with tempfile.TemporaryDirectory()as folder:
            root=Path(folder);data=b'<public>source</public>'
            packed=compress(data,store_size=False)
            archive=b'SFC\x1a'+struct.pack('<II',3,0)+bytes(16)
            archive+=struct.pack('<I',len(packed))+packed+struct.pack('<I',len(data))
            (root/'test.sfc').write_bytes(archive)
            record=dict(path='DATA/test.xml',source='test.sfc',offset=32,
                        storage='sfc_lz4',size=len(data),sha256=hashlib.sha256(data).hexdigest())
            self.assertEqual(read_resource(root,record),data)
            record['size']+=1
            with self.assertRaises(ValueError):read_resource(root,record)
