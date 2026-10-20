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


class TerrainSegmentTests(unittest.TestCase):
    """Аналитические поверхности; не копия алгоритма обхода клеток."""
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path=Path(self.folder.name)/'samples'

    def field(self, heights, flags=2, material2=3):
        self.path.write_bytes(b''.join(struct.pack('<hBB',h,flags,material2)
                                      for row in heights for h in row))
        return HeightField(self.path,len(heights),len(heights[0]),0,0,0,0,1,1)

    def test_vertical_plane_both_directions_and_distinct_faces(self):
        f=self.field([[0,1],[2,3]])  # z=x+2y
        a=f.intersect_segment((.2,.3,10),(.2,.3,-10))
        self.assertAlmostEqual(a['position'][2],.8)
        self.assertAlmostEqual(a['fraction'],.46)
        self.assertEqual(a['face_index'],0)
        self.assertEqual(a['material_index'],2)
        b=f.intersect_segment((.8,.7,-10),(.8,.7,10))
        self.assertAlmostEqual(b['position'][2],2.2)
        self.assertEqual(b['face_index'],1)
        self.assertEqual(b['material_index'],3)
        for actual,expected in zip(b['normal'],(-1/math.sqrt(6),-2/math.sqrt(6),1/math.sqrt(6))):
            self.assertAlmostEqual(actual,expected)

    def test_horizontal_ray_crosses_ridge_in_later_cell(self):
        f=self.field([[0,0,2,0],[0,0,2,0]])
        result=f.intersect_segment((.1,.3,1),(2.9,.3,1))
        self.assertAlmostEqual(result['position'][0],1.5)
        self.assertEqual(result['column'],1)
        self.assertEqual(result['visited_cells'],2)
        backward=f.intersect_segment((2.9,.3,1),(.1,.3,1))
        self.assertAlmostEqual(backward['position'][0],2.5)

    def test_nonplanar_cell_uses_triangles_not_bilinear_surface(self):
        f=self.field([[0,0],[0,8]])
        low=f.intersect_segment((.2,.2,10),(.2,.2,-1))
        high=f.intersect_segment((.8,.8,10),(.8,.8,-1))
        self.assertAlmostEqual(low['position'][2],0)
        self.assertAlmostEqual(high['position'][2],4.8)

    def test_boundary_vertex_endpoint_and_no_intersection(self):
        f=self.field([[0,0,0],[0,0,0],[0,0,0]])
        result=f.intersect_segment((.1,.1,1),(1.9,1.9,-1))
        self.assertAlmostEqual(result['position'][0],1)
        self.assertAlmostEqual(result['position'][1],1)
        self.assertAlmostEqual(result['position'][2],0)
        self.assertAlmostEqual(f.intersect_segment((.5,.5,1),(.5,.5,0))['fraction'],1)
        self.assertEqual(f.intersect_segment((.5,.5,0),(.5,.5,1))['fraction'],0)
        self.assertIsNone(f.intersect_segment((.1,.1,1),(1.9,1.9,1)))
        self.assertIsNone(f.intersect_segment((.1,.1,0),(1.9,1.9,0)))

    def test_invalid_outside_and_unknown_surface_fail_closed(self):
        f=self.field([[0,0],[0,0]])
        for a,b in [((True,0,1),(.5,.5,-1)),((.5,.5,math.nan),(.5,.5,-1)),
                    ((.5,.5,1),(.5,.5,1)),((.5,.5,1),(1,.5,-1))]:
            with self.subTest(a=a,b=b),self.assertRaises(ValueError):f.intersect_segment(a,b)
        for flag in (128,127):
            f=self.field([[0,0],[0,0]],flags=flag)
            with self.assertRaises(ValueError):f.intersect_segment((.5,.5,1),(.5,.5,-1))
        self.path.write_bytes(b'\0'*12)
        with self.assertRaises(ValueError):f.intersect_segment((.5,.5,1),(.5,.5,-1))
