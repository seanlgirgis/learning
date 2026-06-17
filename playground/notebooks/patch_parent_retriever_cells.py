"""Fix Parent Document Retriever + RetrievalQA notebook cells."""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parent / "sean_langchain_lab.ipynb"

CELL_136 = """# >>> LOCAL 1.x | CELL: ParentDocumentRetriever imports | lab: 32.parent_document_retriever.py
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import InMemoryStore
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
"""

CELL_137 = """# >>> LOCAL 1.x | CELL: Parent splitters + Chroma + InMemoryStore
# Needs: document (PDF list) + watsonx_embedding from embeddings cell above

parent_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=20, separator="\\n")
child_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=20, separator="\\n")

vectorstore = Chroma(
    collection_name="split_parents",
    embedding_function=watsonx_embedding,
)
store = InMemoryStore()
"""

PREREQ_MD = """**Run before Parent Document Retriever cells:**
1. `CELL: PDF loader` → variable `document`
2. Embeddings cell → `watsonx_embedding` + `embed_params`
3. (For RetrievalQA below) `CELL: Chroma.from_documents` → `docsearch` + `llama_llm` from setup
"""

CELL_152_HEADER = """# >>> LOCAL 1.x | CELL: RetrievalQA | lab: 31.rag.retrieval_qa.py
# Needs: docsearch (from Chroma.from_documents cell) + llama_llm
"""


def _lines(text: str) -> list[str]:
    parts = text.splitlines(keepends=True)
    return parts if parts else [text]


def main() -> None:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

    # insert prereq markdown before Parent doc header (cell 134)
    if PREREQ_MD not in "".join(nb["cells"][134].get("source", [])):
        for i, c in enumerate(nb["cells"]):
            if "".join(c.get("source", [])).strip() == "##### **Parent document retrievers**":
                nb["cells"].insert(i, {"cell_type": "markdown", "metadata": {}, "source": _lines(PREREQ_MD)})
                break

    # re-find indices after possible insert
    for i, c in enumerate(nb["cells"]):
        src = "".join(c.get("source", []))
        if src.startswith("# >>> LOCAL 1.x | CELL: ParentDocumentRetriever imports"):
            nb["cells"][i]["source"] = _lines(CELL_136)
            nb["cells"][i]["outputs"] = []
            nb["cells"][i]["execution_count"] = None
        elif "parent_splitter = CharacterTextSplitter" in src and "vectorstore = Chroma" in src:
            nb["cells"][i]["source"] = _lines(CELL_137)
            nb["cells"][i]["outputs"] = []
            nb["cells"][i]["execution_count"] = None
        elif "qa = RetrievalQA.from_chain_type" in src:
            if "Needs: docsearch" not in src:
                nb["cells"][i]["source"] = _lines(CELL_152_HEADER + src.lstrip())
                nb["cells"][i]["outputs"] = []
                nb["cells"][i]["execution_count"] = None

    # update study map banner if present
    for c in nb["cells"]:
        src = "".join(c.get("source", []))
        if "LOCAL study map" in src and "32.parent_document_retriever" not in src:
            src = src.replace(
                "| RetrievalQA | `langchain/31.rag.retrieval_qa.py` |",
                "| Parent doc retriever | `langchain/32.parent_document_retriever.py` |\n"
                "| RetrievalQA | `langchain/31.rag.retrieval_qa.py` |",
            )
            c["source"] = _lines(src)

    NOTEBOOK.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print("Patched parent retriever + RetrievalQA cells in", NOTEBOOK.name)


if __name__ == "__main__":
    main()