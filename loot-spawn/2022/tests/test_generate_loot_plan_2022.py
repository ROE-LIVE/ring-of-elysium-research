"""Квоты, воспроизводимость и явное ограничение локального пула."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from generate_loot_plan_2022 import generate


class LootPlanTests(unittest.TestCase):
    def setUp(self):
        self.control = dict(iID='3',iMapID='16010',iRadius='200',num_percent_array=[100])
        self.items = [dict(iID='11',iItemID='10402',iCount='2'),
                      dict(iID='12',iItemID='201001',iCount='1')]

    def test_h2_consumes_quotas_without_replacement_and_never_refills(self):
        points = [(10,20,30)]*3
        plan = generate(self.control,self.items,points,17,'H2')
        self.assertEqual(plan['remaining_quotas'],[0,0])
        self.assertEqual(sorted(x['item_id'] for x in plan['entities']),[10402,10402,201001])
        self.assertEqual(plan,generate(self.control,self.items,points,17,'H2'))
        with self.assertRaises(ValueError):
            generate(self.control,self.items,points+[(10,20,30)],17,'H2')

    def test_h1_is_unbounded_but_restriction_and_positions_are_declared(self):
        plan = generate(self.control,self.items,[(0,0,42)]*20,7,'H1',allowed=[10402])
        self.assertEqual(len(plan['entities']),20)
        self.assertTrue(plan['renormalized_weights'])
        self.assertFalse(plan['original_positions_available'])
        self.assertFalse(plan['original_algorithm_verified'])
        self.assertTrue(all(x['item_id']==10402 and x['position'][2]==42 for x in plan['entities']))

    def test_empty_pool_invalid_policy_and_points_are_rejected(self):
        for policy,points,allowed in [('H0',[(0,0,0)],None),('H2',[],None),
                                      ('H2',[(float('nan'),0,0)],None),('H2',[(0,0,0)],[999])]:
            with self.assertRaises(ValueError):
                generate(self.control,self.items,points,1,policy,allowed=allowed)

    def test_primary_stack_count_comes_from_table_instead_of_one_unit(self):
        items = [dict(iID='11', iItemID='30004', iCount='1', iStackCount='10')]
        plan = generate(self.control, items, [(0, 0, 0)], 7, 'H1')
        self.assertEqual(plan['entities'][0]['quantity'], 10)
        with self.assertRaises(ValueError):
            generate(self.control, [dict(items[0], iStackCount='0')], [(0, 0, 0)], 7, 'H1')

    def test_exact_coordinate_mode_keeps_extras_on_authored_surface(self):
        control = dict(self.control, iRadius='0')
        items = [dict(iID='11', iItemID='10201', iCount='1',
                      iExtraItemID1='30001', iExtraItemWeight1='100',
                      iExtraItemCount1='2', iExtraItemStackCount1='30')]
        point = (416298, 557175, 259802)
        exact = generate(control, items, [point], 17, 'H1', bundle_spacing_cm=0)
        self.assertEqual([row['position'] for row in exact['entities']], [list(point)] * 3)
        self.assertEqual([row['quantity'] for row in exact['entities']], [1, 30, 30])
        legacy = generate(control, items, [point], 17, 'H1')
        self.assertEqual([row['position'][0] for row in legacy['entities']],
                         [point[0], point[0]+45, point[0]+90])
        self.assertFalse(exact['original_algorithm_verified'])
        for spacing in (-1, 201, True, 0.5):
            with self.assertRaises(ValueError):
                generate(control, items, [point], 17, 'H1', bundle_spacing_cm=spacing)
