"""M3 Step 01 — Document class (01.md).

Run from lab/module3:
  python steps/01_document_class.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from llama_index.core import Document


def main() -> None:
    doc = Document(
        text="Hello LlamaIndex",
        metadata={"source": "demo", "topic": "m3-step01"},
    )
    print("Document fields:")
    print(f"  id_: {doc.id_!r}")
    print(f"  metadata: {doc.metadata!r}")
    print(f"  text: {doc.text[:60]!r}...")
    rel = getattr(doc, "relationships", None)
    if rel is not None:
        print(f"  relationships: {rel!r}")
    print("\nIdea: Document = whole source before chunking.")


if __name__ == "__main__":
    main()