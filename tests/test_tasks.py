"""Проверки переносимого CSV и отказа при повреждении этапов."""
import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('tasks', ROOT/'tools/tasks.py')
tasks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tasks)


class TaskTests(unittest.TestCase):
    def test_current_plan_keeps_stable_ids(self):
        rows = tasks.load_plan()
        self.assertEqual(len(rows), 115)
        gun = next(r for r in rows if r['id'] == 'GUN07')
        self.assertEqual(gun['work_state'], 'external_blocked')
        self.assertIn('140D095D6', gun['next_step'])

    def test_bad_stage_does_not_pass_validation(self):
        rows = tasks.load_plan()
        rows[0]['contract'] = '3'
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'plan.csv'
            with path.open('w', encoding='utf-8-sig', newline='') as target:
                writer = csv.DictWriter(target, fieldnames=list(rows[0]), delimiter=';')
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(ValueError):
                tasks.load_plan(path)
