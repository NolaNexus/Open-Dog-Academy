import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_SRC = REPO_ROOT / "scripts" / "validate_status_taxonomy.py"


def run_py(repo_root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "validate_status_taxonomy.py")],
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )


class TestValidateStatusTaxonomy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        (self.root / "scripts").mkdir()
        (self.root / "docs" / "skills" / "ob").mkdir(parents=True)
        (self.root / "docs" / "classes").mkdir(parents=True)
        (self.root / "docs" / "_atoms" / "protocols").mkdir(parents=True)

        shutil.copy2(SCRIPT_SRC, self.root / "scripts" / "validate_status_taxonomy.py")

        # Skill: valid
        (self.root / "docs" / "skills" / "ob" / "OB_TEST.md").write_text(
            """# OB_TEST\n\n**Type:** skill reference\n**Status:** draft\n**Last updated:** 2026-01-10\n\n---\n\nBody\n""",
            encoding="utf-8",
        )

        # Class doc: valid
        (self.root / "docs" / "classes" / "class-guide-test.md").write_text(
            """# Class Guide Test\nStatus: stub\n\nBody\n""",
            encoding="utf-8",
        )

        # Atom (headers are validated by validate_atoms.py, but we still need Status here)
        (self.root / "docs" / "_atoms" / "protocols" / "session-structure-001.md").write_text(
            """ID: `protocol-session-001`\nType: protocol\nStatus: stable\nPath: `docs/_atoms/protocols/session-structure-001.md`\n\n---\n\nBody\n""",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_tree_passes(self):
        res = run_py(self.root)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_invalid_status_fails(self):
        p = self.root / "docs" / "classes" / "class-guide-test.md"
        p.write_text("# Class Guide Test\nStatus: draft (modular refactor)\n", encoding="utf-8")

        res = run_py(self.root)
        self.assertNotEqual(res.returncode, 0)


if __name__ == "__main__":
    unittest.main()
