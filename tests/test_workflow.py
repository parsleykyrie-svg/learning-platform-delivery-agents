import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module
status, gate = load('feature_status'), load('run_checks')

class WorkflowTests(unittest.TestCase):
    def test_stage_must_match_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); p = root/'features/planned/readability.md'; p.parent.mkdir(parents=True)
            p.write_text('---\nfeature: readability\nstage: built\n---\n')
            with self.assertRaises(ValueError): status.collect(root)
            p.write_text('---\nfeature: readability\nstage: planned\n---\n')
            self.assertEqual(status.collect(root)[0]['stage'], 'planned')
    def test_duplicate_trackers_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for stage in ['planned','built']:
                p=root/f'features/{stage}/readability.md';p.parent.mkdir(parents=True)
                p.write_text(f'feature: readability\nstage: {stage}\n')
            with self.assertRaises(ValueError):status.collect(root)
    def test_empty_and_shell_checks_rejected(self):
        for checks in [[],['echo success']]:
            with self.assertRaises(ValueError):gate.run({'checks':checks},ROOT)
    def test_failure_is_not_reported_as_success(self):
        with self.assertRaises(subprocess.CalledProcessError):
            gate.run({'source_directory':'.','checks':[[sys.executable,'-c','raise SystemExit(3)']]},ROOT)
    def test_configured_check_runs(self):
        gate.run({'source_directory':'.','checks':[[sys.executable,'-c','assert 2 + 2 == 4']]},ROOT)

if __name__ == '__main__':unittest.main()
