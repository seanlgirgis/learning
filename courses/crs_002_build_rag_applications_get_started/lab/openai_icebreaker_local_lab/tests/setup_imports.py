"""Test import helper — add project root before ``config`` / ``modules`` imports.

Run tests from the project folder::

    python tests/test_data_extraction.py

Without this file, Python only sees the ``tests/`` folder on the path and
``from modules...`` fails.

OpenAI: No.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))