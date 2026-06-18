"""Capstone 01B — Chat: load saved Chroma → answer questions (you type every bite).

Requires capstone_01_ingest.py run first.

Pre-read: capstone/capstone01.md

Bites:
  1. Imports + CHROMA_DIR (must match ingest script)
  2. Guard — exit with message if CHROMA_DIR missing
  3. Chroma(persist_directory=..., embedding_function=...)  # load, not from_documents
  4. as_retriever + RetrievalQA + make_watsonx_llm()
  5. main — argv question and/or input() loop until quit

Run set_env.ps1 (network for LLM).

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\capstone\\capstone_01_chat.py "What is this paper discussing?"
"""

import sys
from pathlib import Path

_LANGCHAIN_ROOT = Path(__file__).resolve().parent.parent
if str(_LANGCHAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN_ROOT))

# Must match capstone_01_ingest.py
CHROMA_DIR = Path(__file__).resolve().parent / "data" / "chroma_01"

DEFAULT_QUESTION = "what is this paper discussing?"


# --- Bite 1: imports ---
# TODO: sys, RetrievalQA, Chroma, EmbedTextParamsMetaNames
#       make_watsonx_embeddings, make_watsonx_llm


# --- Bite 2: guard ---
# TODO: if not CHROMA_DIR.exists(): print("Run capstone_01_ingest.py first"); sys.exit(1)


# --- Bite 3: load store ---
# TODO: embedding_model = make_watsonx_embeddings(same params as ingest)
#       vector_store = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embedding_model)


# --- Bite 4: QA chain ---
# TODO: retriever = vector_store.as_retriever(search_kwargs={"k": 3})
#       qa = RetrievalQA.from_chain_type(llm=make_watsonx_llm(), ...)


# --- Bite 5: main ---
def main() -> None:
    # TODO: one-shot from sys.argv[1] OR REPL: while (q := input("Q: ")) not in ("quit", "exit"): ...
    raise NotImplementedError("Fill bites 1–5 — see capstone01.md")


if __name__ == "__main__":
    main()