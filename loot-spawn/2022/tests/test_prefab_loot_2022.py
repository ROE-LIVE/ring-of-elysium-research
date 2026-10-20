"""Геометрия исходных узлов и повторяемость собственной политики H1."""
import copy
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from audit_prefab_loot_nodes_2022 import world_point
from generate_prefab_loot_catalog_2022 import build


class PrefabLootTests(unittest.TestCase):
    def test_rotation_uses_scaled_local_before_translation(self):
        instance=ET.fromstring('<LayoutInstance><mPosition x="100" y="200" z="300"/>'
          '<mScale x="2" y="3" z="4"/><mRotMatrix><m>'
          '<m x="0" y="-1" z="0"/><m x="1" y="0" z="0"/><m x="0" y="0" z="1"/>'
          '</m></mRotMatrix></LayoutInstance>')
        self.assertEqual(world_point(instance,(5,7,11)),(79,210,344))

    def inputs(self):
        nodes=[dict(Index=i+1,Controller=3,X=i*100,Y=200,Z=300,position_verified=True,
                    Instance=i,Node='node_1',Prefab='Data.layout.prefab.test') for i in range(20)]
        tables=dict(control=dict(rows=[dict(iID='3',iMapID='16010',num_percent_array=[100])]),
                    items=dict(rows=[dict(iID='11',iCtrlID='3',iItemID='10402',iCount='1'),
                                     dict(iID='12',iCtrlID='3',iItemID='10201',iCount='1')]))
        return nodes,tables

    def test_seed_reproduces_and_original_xyz_do_not_scatter(self):
        nodes,tables=self.inputs();first=build(nodes,tables,17)
        self.assertEqual(first,build(list(reversed(nodes)),tables,17))
        self.assertNotEqual(first['entities'],build(nodes,tables,18)['entities'])
        self.assertEqual(len(first['entities']),20)
        self.assertTrue(all(item['position']==[(item['source_point_id']-1)*100,200,300] for item in first['entities']))
        self.assertFalse(first['original_algorithm_verified'])
        self.assertFalse(first['controller_binding_verified'])

    def test_unverified_duplicates_bad_bounds_and_empty_result_rejected(self):
        nodes,tables=self.inputs()
        for rows,seed,bounds in ((nodes,True,None),(nodes,17,[0,0,0,1]),
              (nodes,17,[10000,10000,11000,11000]),(nodes+[nodes[0]],17,None)):
            with self.assertRaises(ValueError):build(rows,tables,seed,bounds)
        rows=copy.deepcopy(nodes);rows[0]['position_verified']=False
        with self.assertRaises(ValueError):build(rows,tables,17)


if __name__=='__main__':unittest.main()
