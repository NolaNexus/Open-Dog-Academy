import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_SRC = REPO_ROOT / "scripts" / "chunk_for_chat.py"

def run_py(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(repo_root / "scripts" / "chunk_for_chat.py"), *args],
                          cwd=str(repo_root),
                          text=True,
                          capture_output=True)

class TestChunkForChat(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "scripts").mkdir()
        (self.root / "docs").mkdir()
        shutil.copy2(SCRIPT_SRC, self.root / "scripts" / "chunk_for_chat.py")

        # Make an include file under docs/_atoms
        (self.root / "docs" / "_atoms" / "templates").mkdir(parents=True)
        (self.root / "docs" / "_atoms" / "templates" / "a.md").write_text("## Included\n\nHELLO\n", encoding="utf-8")

        # Source document with includes + multiple H2 sections
        src = (
            "# Title\n\n"
            "--8<-- \"_atoms/templates/a.md\"\n\n"
            "## Section 1\n\n" + ("A" * 2000) + "\n\n"
            "## Section 2\n\n" + ("B" * 2000) + "\n\n"
        )
        (self.root / "docs" / "src.md").write_text(src, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_chunks_created_and_end_markers_present(self):
        out = self.root / "docs" / "out"
        res = run_py(self.root, "docs/src.md", "--max-chars", "2500", "--out", str(out), "--expand-includes")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

        index = out / "index.md"
        self.assertTrue(index.exists())

        parts = sorted(out.glob("part-*.md"))
        self.assertGreaterEqual(len(parts), 2)

        for p in parts:
            txt = p.read_text(encoding="utf-8")
            self.assertIn("<!-- END_OF_PART", txt)
            # part body should not exceed max_chars too much; header adds overhead, so just sanity-check
            self.assertLess(len(txt), 8000)

        # included content should appear in part 1 (expanded)
        first = parts[0].read_text(encoding="utf-8")
        self.assertIn("HELLO", first)

if __name__ == "__main__":
    unittest.main()
