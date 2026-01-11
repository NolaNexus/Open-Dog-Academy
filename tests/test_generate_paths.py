import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class TestGeneratePaths(unittest.TestCase):
    def test_generate_then_check_clean(self):
        r1 = subprocess.run(["python3", "scripts/generate_paths.py"], cwd=REPO_ROOT)
        self.assertEqual(r1.returncode, 0)

        r2 = subprocess.run(["python3", "scripts/generate_paths.py", "--check"], cwd=REPO_ROOT)
        self.assertEqual(r2.returncode, 0)


if __name__ == "__main__":
    unittest.main()
