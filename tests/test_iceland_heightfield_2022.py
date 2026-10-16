"""Треугольная интерполяция и границы point reader без игровых ресурсов."""
import math
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from probe_iceland_heightfield_2022 import HeightField,interpolate_height,height_gradient


class HeightFieldTests(unittest.TestCase):
    def samples(self,flag):return [(0,flag,7),(10,1,1),(20,1,1),(60,1,1)]
    def test_opposite_diagonal_triangles(self):
        self.assertEqual(interpolate_height(self.samples(0),.2,.3),7)
        self.assertEqual(interpolate_height(self.samples(0),.8,.7),38)
        self.assertEqual(height_gradient(self.samples(0),.5,.5),(50,40))
    def test_tessellation_diagonal_changes_nonplanar_cell(self):
        self.assertEqual(interpolate_height(self.samples(128),.2,.3),13)
        self.assertEqual(interpolate_height(self.samples(128),.8,.7),44)
    def test_world_transform_signed_heights_and_hole_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'samples';path.write_bytes(b''.join(struct.pack('<hBB',h,127,2) for h in (-10,-8,-6,-4)))
            field=HeightField(path,2,2,0,100,200,300,10,2)
            result=field.height_at(105,205)
            self.assertEqual(result['terrain_z'],286)
            self.assertTrue(result['possible_hole'])
            self.assertEqual(result['material_pair'],(127,2))
            self.assertEqual(result['face_index'],1)
            self.assertEqual(result['material_index'],2)
    def test_nonfinite_and_outside_points_rejected_before_open(self):
        field=HeightField(Path('absent'),2,2,0,0,0,0,1,1)
        for point in ((math.nan,0),(0,math.inf),(-.1,0),(1,0),(0,1),(True,0)):
            with self.subTest(point=point),self.assertRaises(ValueError):field.height_at(*point)
    def test_truncated_samples_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'samples';path.write_bytes(b'\0'*12)
            with self.assertRaises(ValueError):HeightField(path,2,2,0,0,0,0,1,1).height_at(.5,.5)
    def test_unknown_asset_size_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'other';path.write_bytes(b'SEBD')
            with self.assertRaises(ValueError):HeightField.load(path)
