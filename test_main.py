"""Tests for main.py: the program must write one short pickup line to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt), exactly one line,
1-200 characters, valid UTF-8, not whitespace-only."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent


def run_main(out_dir: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["MAKEFUN_OUTPUT_DIR"] = str(out_dir)
    return subprocess.run(
        [sys.executable, str(REPO / "main.py")],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestPickupLine(unittest.TestCase):
    def test_writes_entry_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            result = run_main(out_dir)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            entry = out_dir / "entry.txt"
            self.assertTrue(entry.exists(), "entry.txt was not written")

    def test_entry_is_one_line_1_to_200_chars(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            result = run_main(out_dir)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            raw = (out_dir / "entry.txt").read_bytes()
            text = raw.decode("utf-8")  # must be valid UTF-8
            body = text.rstrip("\n")
            self.assertNotIn("\n", body, "entry must be a single line")
            self.assertGreaterEqual(len(body), 1, "entry must not be empty")
            self.assertLessEqual(len(body), 200, "entry must be <= 200 chars")
            self.assertTrue(body.strip(), "entry must not be whitespace-only")

    def test_deterministic_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "a"
            second = Path(tmp) / "b"
            first.mkdir()
            second.mkdir()
            self.assertEqual(run_main(first).returncode, 0)
            self.assertEqual(run_main(second).returncode, 0)
            self.assertEqual(
                (first / "entry.txt").read_bytes(),
                (second / "entry.txt").read_bytes(),
                "output must be deterministic across runs",
            )


if __name__ == "__main__":
    unittest.main()
