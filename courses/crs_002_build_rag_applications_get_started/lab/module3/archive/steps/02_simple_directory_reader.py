"""M3 Step 02 — SimpleDirectoryReader (01.md, quiz Q3).

Run:
  python steps/02_simple_directory_reader.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from llama_index.core import SimpleDirectoryReader

from lib.m3_shared import SAMPLE_DOCS_DIR


def main() -> None:
    base = str(SAMPLE_DOCS_DIR)
    print(base)     
    print("=== All files in sample_docs ===")
    docs_all = SimpleDirectoryReader(base,recursive=True).load_data()
    for d in docs_all:
        print(f"  - {d.metadata.get('file_name')} ({len(d.text)} chars)")

    print("\n=== recursive=True + required_exts .csv and .json only ===")
    docs_filtered = SimpleDirectoryReader(
        base,
        recursive=True,
        required_exts=[".csv", ".json"],
    ).load_data()
    for d in docs_filtered:
        print(f"  - {d.metadata.get('file_name')}")

    print("\nQuiz pattern: recursive=True + required_exts=[\".csv\", \".json\"]")


if __name__ == "__main__":
    main()