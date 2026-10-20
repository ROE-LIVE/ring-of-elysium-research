"""Полные опубликованные данные и запрет записи в исходный клиент."""
from pathlib import Path
import hashlib,json,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from generate_catalog import load_inputs
from generate_prefab_loot_catalog_2022 import build
from export_source_from_client import validate_destinations


class PublicLootBundleTests(unittest.TestCase):
    def test_published_points_reproduce_both_recorded_catalogs(self):
        nodes,tables=load_inputs(ROOT/'data');self.assertEqual(len(nodes),7155)
        records=json.loads((ROOT/'evidence/current-generation-checks.json').read_text())
        for expected in records['results']:
            catalog=build(nodes,tables,expected['seed'])
            digest=hashlib.sha256(json.dumps(catalog,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            self.assertEqual(digest,expected['full_catalog_canonical_sha256'])
            self.assertEqual(len(catalog['entities']),expected['full_entities'])
            self.assertEqual(catalog,build(list(reversed(nodes)),tables,expected['seed']))
            self.assertFalse(catalog['original_algorithm_verified'])
            self.assertFalse(catalog['controller_binding_verified'])

    def test_refresh_rejects_client_overlap_existing_directories_and_symlink(self):
        with tempfile.TemporaryDirectory()as folder:
            root=Path(folder);client=root/'client';client.mkdir();marker=client/'keep';marker.write_bytes(b'original')
            for cache,output in [(client/'cache',root/'out'),(root/'cache',client/'out'),(root,root/'out'),(root/'cache',root/'cache/out')]:
                with self.assertRaises(ValueError):validate_destinations(client,cache,output)
            link=root/'link';link.symlink_to(client,target_is_directory=True)
            with self.assertRaises(ValueError):validate_destinations(client,root/'cache',link/'out')
            self.assertEqual(marker.read_bytes(),b'original');self.assertEqual(list(client.iterdir()),[marker])
            a,b,c=validate_destinations(client,root/'cache',root/'out')
            self.assertEqual((a,b,c),(client,root/'cache',root/'out'))
