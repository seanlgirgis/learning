"""Import bootstrap — add project root to ``sys.path``.

When you run ``python main.py`` or ``python tests/test_*.py``, Python needs the
project folder on the path so ``import config`` and ``from modules...`` work.

This file runs automatically when ``main.py``, ``app.py``, or ``modules`` load.
Tests use ``tests/setup_imports.py`` for the same job.

OpenAI: No.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def ensure_project_root_on_path() -> Path:
    """Add the lab folder to ``sys.path`` if it is not already there.

    What it does:
        Inserts ``PROJECT_ROOT`` at the front of ``sys.path``.

    Inputs:
        None.

    Returns:
        Path to the project root directory.

    OpenAI:
        No.
    """
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    return PROJECT_ROOT


ensure_project_root_on_path()