"""The Perfect Pickup Line — make.fun entry.

Writes one short pickup line an AI agent could say out loud to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when unset).

The line: an agent built to predict the next word, asking the person
to surprise it instead — with a yes.
"""

import os
from pathlib import Path

# Revised: tighter spoken rhythm — the "yes" itself is the surprise.
LINE = "I was built to predict your next word, so go ahead \u2014 surprise me with a yes."


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_text(LINE, encoding="utf-8")


if __name__ == "__main__":
    main()
