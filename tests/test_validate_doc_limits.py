import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_SRC = REPO_ROOT / "scripts" / "validate_doc_limits.py"

def run_py(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(repo_root / "scripts" / "validate_doc_limits.py"), *args],
                          cwd=str(repo_root),
                          text=True,
                          capture_output=True)

class TestValidateDocLimits(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "scripts").mkdir()
        (self.root / "docs").mkdir()
        shutil.copy2(SCRIPT_SRC, self.root / "scripts" / "validate_doc_limits.py")

    def tearDown(self):
        self.tmp.cleanup()

    def write_config(self, yml: str):
        (self.root / "doc-limits.yml").write_text(yml, encoding="utf-8")

    def write_doc(self, rel: str, content: str):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def test_no_docs_passes(self):
        self.write_config("defaults:\n  max_chars: 100\n  max_lines: 10\nrules: []\n")
        res = run_py(self.root)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_exactly_at_limit_passes(self):
        self.write_config("defaults:\n  max_chars: 10\n  max_lines: 2\nrules: []\n")
        # 10 chars incl newline? keep simple: 9 + '\n' = 10
        self.write_doc("docs/a.md", "123456789\n")
        res = run_py(self.root)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_over_limit_fails(self):
        self.write_config("defaults:\n  max_chars: 5\n  max_lines: 10\nrules: []\n")
        self.write_doc("docs/a.md", "123456\n")
        res = run_py(self.root)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("VIOLATION", res.stdout + res.stderr)

    def test_warn_threshold_no_fail(self):
        self.write_config(
            "defaults:\n"
            "  max_chars: 100\n"
            "  max_lines: 100\n"
            "  warn_ratio: 0.50\n"
            "rules: []\n"
        )
        self.write_doc("docs/a.md", "x" * 60)
        res = run_py(self.root)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("WARNING", res.stdout + res.stderr)

    def test_fail_on_warn_exit_code_2(self):
        self.write_config(
            "defaults:\n"
            "  max_chars: 100\n"
            "  max_lines: 100\n"
            "  warn_ratio: 0.50\n"
            "rules: []\n"
        )
        self.write_doc("docs/a.md", "x" * 60)
        res = run_py(self.root, "--fail-on-warn")
        self.assertEqual(res.returncode, 2, res.stdout + res.stderr)

    def test_rules_precedence_first_match_wins(self):
        self.write_config(
            "defaults:\n  max_chars: 100\n  max_lines: 100\n"
            "rules:\n"
            "  - name: first\n"
            "    globs: ['docs/special/*.md']\n"
            "    max_chars: 10\n"
            "    max_lines: 100\n"
            "  - name: second\n"
            "    globs: ['docs/**/*.md']\n"
            "    max_chars: 5\n"
            "    max_lines: 100\n"
        )
        self.write_doc("docs/special/a.md", "123456789\n")  # 10 chars -> ok for first, would violate second
        res = run_py(self.root)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_overrides_win(self):
        self.write_config(
            "defaults:\n  max_chars: 5\n  max_lines: 100\n"
            "rules: []\n"
            "overrides:\n"
            "  - name: big\n"
            "    path: docs/a.md\n"
            "    max_chars: 20\n"
            "    max_lines: 100\n"
        )
        self.write_doc("docs/a.md", "123456789\n")
        res = run_py(self.root)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_exclude_glob_ignored(self):
        self.write_config(
            "defaults:\n  max_chars: 5\n  max_lines: 100\n"
            "exclude_globs:\n  - 'docs/ignore/*.md'\n"
            "rules: []\n"
        )
        self.write_doc("docs/ignore/a.md", "123456789\n")  # huge but excluded
        res = run_py(self.root)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

if __name__ == "__main__":
    unittest.main()
