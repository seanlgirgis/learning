"""Patch sean_langchain_lab.ipynb for LangChain 1.x + LOCAL cell markers."""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parent / "sean_langchain_lab.ipynb"
MARKER = "# >>> LOCAL 1.x"

REPLACEMENTS = [
    ("from langchain.text_splitter import", "from langchain_text_splitters import"),
    ("from langchain.vectorstores import Chroma", "from langchain_community.vectorstores import Chroma"),
    ("from langchain.retrievers import ParentDocumentRetriever", "from langchain_classic.retrievers import ParentDocumentRetriever"),
    ("from langchain.storage import InMemoryStore", "from langchain_classic.storage import InMemoryStore"),
    ("retriever.get_relevant_documents(", "retriever.invoke("),
    ("from langchain.memory import", "from langchain_classic.memory import"),
    ("from langchain.chains import", "from langchain_classic.chains import"),
    ("from langchain.tools import tool", "from langchain_classic.tools import tool"),
    ("from langchain.agents import", "from langchain_classic.agents import"),
    (
        "# Import BaseModel and Field from langchain_core's pydantic_v1 module",
        "# Import BaseModel and Field from pydantic (LangChain 1.x)",
    ),
]

# cell_index -> header lines prepended to code cells (if not already marked)
CELL_HEADERS: dict[int, str] = {
    94: "# >>> LOCAL 1.x | CELL: PDF loader (PyPDFLoader) | lab: 24.loader.pdf.py\n",
    100: "# >>> LOCAL 1.x | CELL: WebBaseLoader | lab: 25.loader.web.py\n",
    105: (
        "# >>> LOCAL 1.x | CELL: CharacterTextSplitter on PDF | lab: 26.splitter.character.py\n"
        "# Note: `document` = list from loader.load() (notebook keeps singular name)\n"
    ),
    109: "# >>> LOCAL 1.x | CELL: Exercise 3 — compare splitters | lab: 27.exercise3.load_split.py\n",
    121: "# >>> LOCAL 1.x | CELL: Chroma import | lab: 29.chroma.store_search.py\n",
    123: "# >>> LOCAL 1.x | CELL: Chroma.from_documents | labs: 28–29\n",
    135: "# >>> LOCAL 1.x | CELL: ParentDocumentRetriever imports | langchain_classic\n",
    151: "# >>> LOCAL 1.x | CELL: RetrievalQA (full RAG answer) | lab: 31.rag.retrieval_qa.py\n",
    153: "# >>> LOCAL 1.x | CELL: Exercise 4 starter — retriever search | lab: 30.exercise.retriever.py\n",
}

DOCUMENTS_BANNER = """---
**LOCAL study map (Sean)** — playground mirrors

| Notebook topic | Script |
|----------------|--------|
| PDF loader | `langchain/24.loader.pdf.py` |
| Web loader | `langchain/25.loader.web.py` |
| Character split | `langchain/26.splitter.character.py` |
| Exercise 3 splitters | `langchain/27.exercise3.load_split.py` |
| Embeddings | `langchain/28.embeddings.demo.py` |
| Chroma search | `langchain/29.chroma.store_search.py` |
| Exercise 4 retriever | `langchain/30.exercise.retriever.py` |
| RetrievalQA | `langchain/31.rag.retrieval_qa.py` |

Code cells marked with `# >>> LOCAL 1.x | CELL: ...` — import fixes for foundation venv.
Import cheat sheet: `playground/langchain/coursera_import_map.md`
---
"""


def _splitlines(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    return lines if lines else [text]


def patch_cell_source(src: str) -> str:
    for old, new in REPLACEMENTS:
        src = src.replace(old, new)
    # fix stale comment on splitter cell
    src = src.replace(
        "# Import the CharacterTextSplitter class from langchain.text_splitter module",
        "# CharacterTextSplitter — import from langchain_text_splitters (1.x)",
    )
    return src


def main() -> None:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    changed = 0
    headers = 0

    # banner after ### Documents (cell 83)
    banner_src = [DOCUMENTS_BANNER]
    if len(nb["cells"]) > 84 and DOCUMENTS_BANNER not in "".join(nb["cells"][84].get("source", [])):
        if "LOCAL study map" not in "".join(nb["cells"][84].get("source", [])):
            nb["cells"].insert(84, {"cell_type": "markdown", "metadata": {}, "source": banner_src})
            changed += 1
            # shift header indices after insert
            shifted_headers = {k + 1 if k >= 84 else k: v for k, v in CELL_HEADERS.items()}
            CELL_HEADERS.clear()
            CELL_HEADERS.update(shifted_headers)

    for idx, cell in enumerate(nb["cells"]):
        src = "".join(cell.get("source", []))
        new_src = patch_cell_source(src)
        if new_src != src:
            cell["source"] = _splitlines(new_src)
            if cell["cell_type"] == "code":
                cell["outputs"] = []
                cell["execution_count"] = None
            changed += 1

        if cell["cell_type"] == "code" and idx in CELL_HEADERS:
            src = "".join(cell.get("source", []))
            if MARKER not in src:
                cell["source"] = _splitlines(CELL_HEADERS[idx] + src)
                headers += 1

    NOTEBOOK.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print(f"Patched {NOTEBOOK.name}: content fixes={changed}, headers={headers}")


if __name__ == "__main__":
    main()