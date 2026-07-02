"""CRS 002 M3 — Redirect: use lab/module3 track.

The full step-by-step Module 3 lab lives in:

  ../module3/README.md

Quick full REPL:

  cd ..\\module3
  python lab_03_icebreaker.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_MODULE3 = Path(__file__).resolve().parents[1] / "module3"
_TARGET = _MODULE3 / "lab_03_icebreaker.py"


def main() -> None:
    print("Forwarding to lab/module3/lab_03_icebreaker.py")
    print("See lab/module3/README.md for labs 01-03.\n")
    raise SystemExit(subprocess.call([sys.executable, str(_TARGET)], cwd=str(_MODULE3)))


if __name__ == "__main__":
    main()