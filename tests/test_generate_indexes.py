import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_SRC = REPO_ROOT / "scripts" / "generate_indexes.py"


def run_py(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "generate_indexes.py"), *args],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )


class TestGenerateIndexes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "scripts").mkdir()
        (self.root / "docs" / "indexes").mkdir(parents=True)
        shutil.copy2(SCRIPT_SRC, self.root / "scripts" / "generate_indexes.py")

        # Minimal docs tree
        (self.root / "docs" / "skills" / "ob").mkdir(parents=True)
        (self.root / "docs" / "classes").mkdir(parents=True)
        (self.root / "docs" / "instructor-guides").mkdir(parents=True)
        (self.root / "docs" / "classes" / "suite").mkdir(parents=True)

        (self.root / "docs" / "skills" / "ob" / "OB_RECALL.md").write_text(
            "# OB_RECALL — Recall\n", encoding="utf-8"
        )
        (self.root / "docs" / "skills" / "ob" / "OB_SIT.md").write_text(
            "# OB_SIT — Sit\n", encoding="utf-8"
        )

        (self.root / "docs" / "classes" / "class-guide-obedience.md").write_text(
            "# Class Guide: Obedience\n", encoding="utf-8"
        )
        (self.root / "docs" / "classes" / "suite" / "index.md").write_text(
            "# Suite Index\n", encoding="utf-8"
        )

        (self.root / "docs" / "instructor-guides" / "level-0.md").write_text(
            "# Level 0\n", encoding="utf-8"
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_write_then_check_is_clean(self):
        res = run_py(self.root)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

        # Should now be clean in --check mode
        res2 = run_py(self.root, "--check")
        self.assertEqual(res2.returncode, 0, res2.stdout + res2.stderr)

        skills_index = (self.root / "docs" / "indexes" / "skills-index.md").read_text(encoding="utf-8")
        self.assertIn("OB_RECALL", skills_index)
        self.assertIn("OB_SIT", skills_index)

        classes_index = (self.root / "docs" / "indexes" / "class-guides-index.md").read_text(encoding="utf-8")
        self.assertIn("Class Guide: Obedience", classes_index)
        self.assertIn("Suite Index", classes_index)

        ig_index = (self.root / "docs" / "indexes" / "instructor-guides-index.md").read_text(encoding="utf-8")
        self.assertIn("Level 0", ig_index)

    def test_check_fails_when_stale(self):
        # Write an obviously wrong index file
        (self.root / "docs" / "indexes" / "skills-index.md").write_text("# wrong\n", encoding="utf-8")
        res = run_py(self.root, "--check")
        self.assertNotEqual(res.returncode, 0)


if __name__ == "__main__":
    unittest.main()
