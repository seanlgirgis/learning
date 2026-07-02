"""Copy CRS 002 M1 RAG notebook and patch for local watson_llm + LangChain 1.x."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parents[2]
SRC = (
    COURSE_ROOT
    / "source_material/module1/Summarize private documents using RAG LangChain and LLMs.ipynb"
)
DST_COURSE = Path(__file__).resolve().parent / "sean_crs002_m1_rag_summarize.ipynb"
DST_PLAYGROUND = (
    Path(__file__).resolve().parents[4] / "playground/notebooks/sean_crs002_m1_rag_summarize.ipynb"
)

LOCAL_SETUP_MD = """### Local setup (CRS 002)

- Run **`D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1`** before Jupyter.
- Start via **`playground/notebooks/start_jupyter.ps1`**.
- LLM + embeddings: **`watson_llm.py`** (OpenAI backend). Skills Network / `project_id = "skills-network"` cells are replaced below.
- Rebuild this file: `lab/notebooks/prepare_m1_rag_notebook.py`
"""

SKIP_PIP_MD = """### Coursera pip cells skipped

Use the **rag_application_builder_foundation** venv (already has langchain, chromadb, etc.).
"""

LOCAL_IMPORTS = """# LOCAL — LangChain 1.x + watson_llm shim
import warnings

warnings.filterwarnings("ignore")

from langchain_classic.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_classic.memory import ConversationBufferMemory
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import CharacterTextSplitter
from watson_llm import make_watsonx_embeddings, make_watsonx_llm

import wget

print("Local imports OK")
"""

LOCAL_EMBED = """# LOCAL — embeddings + Chroma (Indexing)
embeddings = make_watsonx_embeddings()
docsearch = Chroma.from_documents(texts, embeddings)
print("document ingested")
"""

LOCAL_LLM = """# LOCAL — single LLM for all notebook cells (course used granite twice)
flan_ul2_llm = make_watsonx_llm()
llama_3_llm = flan_ul2_llm
print("LLM ready:", type(flan_ul2_llm).__name__)
"""

SKIP_WATSONX_MD = """### IBM watsonx.ai Model() block skipped locally

See **LOCAL LLM** cell above (`make_watsonx_llm`).
"""


def _set_cell_source(cell: dict, text: str, cell_type: str = "code") -> None:
    cell["cell_type"] = cell_type
    lines = text if text.endswith("\n") else text + "\n"
    cell["source"] = [line if line.endswith("\n") else line + "\n" for line in lines.splitlines()]
    cell["outputs"] = []
    if cell_type == "code":
        cell["execution_count"] = None


def patch_notebook(nb: dict) -> None:
    cells = nb["cells"]

    # After "## Setup" markdown (cell 9), insert local setup note at 10
    cells.insert(10, {"cell_type": "markdown", "metadata": {}, "source": [LOCAL_SETUP_MD]})

    # pip install cell → skip markdown
    for i, cell in enumerate(cells):
        src = "".join(cell.get("source", []))
        if cell["cell_type"] == "code" and "%%capture" in src and "ibm-watsonx-ai" in src:
            _set_cell_source(cell, SKIP_PIP_MD, "markdown")
        elif cell["cell_type"] == "code" and "pip list" in src:
            _set_cell_source(cell, "# LOCAL: pip check skipped\n", "code")
        elif cell["cell_type"] == "code" and "from langchain.document_loaders import TextLoader" in src:
            _set_cell_source(cell, LOCAL_IMPORTS, "code")
        elif cell["cell_type"] == "code" and "HuggingFaceEmbeddings()" in src:
            _set_cell_source(cell, LOCAL_EMBED, "code")
        elif cell["cell_type"] == "code" and src.strip().startswith("model_id = 'ibm/granite"):
            if "llama_3_llm = WatsonxLLM" in src:
                _set_cell_source(cell, "# LOCAL: second model block merged into LOCAL_LLM cell\n", "code")
            else:
                _set_cell_source(cell, LOCAL_LLM, "code")
        elif cell["cell_type"] == "code" and "credentials = {" in src and "skills-network" in src:
            _set_cell_source(cell, SKIP_WATSONX_MD, "markdown")
        elif cell["cell_type"] == "code" and "model = Model(" in src:
            _set_cell_source(cell, "# LOCAL: Model() skipped\n", "code")
        elif cell["cell_type"] == "code" and "flan_ul2_llm = WatsonxLLM" in src:
            _set_cell_source(cell, "# LOCAL: WatsonxLLM skipped — see LOCAL_LLM cell\n", "code")


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Source notebook not found: {SRC}")

    nb = json.loads(SRC.read_text(encoding="utf-8"))
    patch_notebook(nb)

    DST_COURSE.parent.mkdir(parents=True, exist_ok=True)
    DST_COURSE.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print(f"Wrote: {DST_COURSE}")

    DST_PLAYGROUND.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(DST_COURSE, DST_PLAYGROUND)
    print(f"Copied: {DST_PLAYGROUND}")


if __name__ == "__main__":
    main()