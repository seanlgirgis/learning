"""Patch Sean notebooks: WATSONX_* wording → OpenAI (watson_llm stealth shim).

Run after provider swap or when refreshing from Coursera:

    python patch_notebooks_openai.py
    python patch_langchain_env.py      # langchain lab — extra cell fixes
"""

from __future__ import annotations

import json
import re
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).resolve().parent

NOTEBOOKS = (
    NOTEBOOK_DIR / "sean_in_context_lab.ipynb",
    NOTEBOOK_DIR / "sean_langchain_lab.ipynb",
    NOTEBOOK_DIR / ".ipynb_checkpoints" / "sean_in_context_lab-checkpoint.ipynb",
    NOTEBOOK_DIR / ".ipynb_checkpoints" / "sean_langchain_lab-checkpoint.ipynb",
)

IN_CONTEXT_LOCAL_NOTE = (
    "> **Local copy:** LLM via **`make_watsonx_llm`** → **OpenAI** (`OPENAI_*` from "
    "`start_jupyter.ps1` / `set_env.ps1`). Coursera `skills-network` / Granite cells skipped.\n"
    "> See [PROVIDER_SWAP_WATSON_TO_OPENAI.md](../langchain/PROVIDER_SWAP_WATSON_TO_OPENAI.md).\n"
)

LANGCHAIN_LOCAL_NOTE = (
    "> **Local copy:** LLM + embeddings via **`watson_llm`** / **`watson_helper`** → **OpenAI** "
    "(`OPENAI_*` from `start_jupyter.ps1`). Not `skills-network` or Coursera demo models.\n"
    "> See [PROVIDER_SWAP_WATSON_TO_OPENAI.md](../langchain/PROVIDER_SWAP_WATSON_TO_OPENAI.md).\n"
)

LOCAL_RUNNING_MD = (
    "### Running Locally\n\n"
    "This copy uses **`start_jupyter.ps1`** (runs `set_env.ps1`). "
    "Helpers **`watson_helper.py`** and **`watson_llm.py`** in `../langchain/` call **OpenAI** "
    "behind watsonx-compatible names (`make_watsonx_llm`, `make_watsonx_embeddings`).\n"
)

MODEL_PRINT = 'print("Model:", __import__("os").environ.get("OPENAI_MODEL", "gpt-4o-mini"))'

HINT_LLM_BLOCK_RE = re.compile(
    r'model_id = "ibm/granite-4-h-small".*?'
    r'llm = WatsonxLLM\(\s*'
    r"model_id=model_id,\s*"
    r"url=url,\s*"
    r"project_id=project_id,\s*"
    r"params=parameters\s*"
    r"\)",
    re.DOTALL,
)

HINT_LLM_REPLACEMENT = """parameters = {
    GenParams.MAX_NEW_TOKENS: 512,
    GenParams.TEMPERATURE: 0.2,
}

from watson_llm import make_watsonx_llm
llm = make_watsonx_llm(parameters)"""

LOCAL_SHIM_IMPORTS = """# LOCAL: OpenAI via watson_llm shim (Coursera used IBM WatsonxLLM / ModelInference)
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from watson_llm import make_watsonx_llm, make_watsonx_embeddings
"""

IBM_RUNTIME_IMPORT_RE = re.compile(
    r"^from ibm_watsonx_ai\.foundation_models import (?:ModelInference|Model)\s*\n"
    r"|^from ibm_watsonx_ai\.foundation_models\.utils\.enums import ModelTypes\s*\n"
    r"|^from langchain_ibm import Watsonx(?:LLM|Embeddings)[^\n]*\n",
    re.MULTILINE,
)


def _strip_ibm_runtime_imports(src: str) -> str:
    """Drop IBM SDK / langchain_ibm imports; keep GenParams + watson_llm shim."""
    src = src.replace("# IBM WatsonX imports\n", LOCAL_SHIM_IMPORTS)

    # Remove runtime IBM / langchain_ibm lines (anywhere in cell)
    drop_line = re.compile(
        r"^from ibm_watsonx_ai\.foundation_models import (?:ModelInference|Model)\s*$",
        re.MULTILINE,
    )
    src = drop_line.sub("", src)
    src = re.sub(
        r"^from ibm_watsonx_ai\.foundation_models\.utils\.enums import ModelTypes\s*$",
        "",
        src,
        flags=re.MULTILINE,
    )
    src = re.sub(
        r"^from langchain_ibm import Watsonx(?:LLM|Embeddings).*$",
        "",
        src,
        flags=re.MULTILINE,
    )

    # Insert shim block after warnings if cell uses LLM stack but has no watson_llm import
    if (
        "make_watsonx_llm" not in src
        and ("PromptTemplate" in src or "LLMChain" in src or "llm_model" in src or "GenParams" in src)
        and LOCAL_SHIM_IMPORTS.strip() not in src
    ):
        src = re.sub(
            r"(warnings\.filterwarnings\([^\n]+\)\n)",
            r"\1\n" + LOCAL_SHIM_IMPORTS,
            src,
            count=1,
        )

    # Deduplicate repeated import lines
    seen: set[str] = set()
    lines: list[str] = []
    for line in src.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("from ") or stripped.startswith("import "):
            if stripped in seen:
                continue
            seen.add(stripped)
        lines.append(line)
    src = "".join(lines)

    # Ensure param helpers when referenced
    if "GenParams" in src and "GenTextParamsMetaNames" not in src:
        src = "from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams\n" + src
    if "embed_params" in src and "EmbedTextParamsMetaNames" not in src:
        src = "from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames\n" + src
    if "make_watsonx_llm" in src and "from watson_llm import" not in src:
        src = "from watson_llm import make_watsonx_llm\n" + src
    if "make_watsonx_embeddings" in src and "make_watsonx_embeddings" not in src.split("from watson_llm import")[0]:
        if "from watson_llm import" not in src:
            src = "from watson_llm import make_watsonx_embeddings\n" + src

    return src


def _splitlines(text: str) -> list[str]:
    if not text:
        return []
    return text.splitlines(keepends=True) if text.endswith("\n") else [
        *text.splitlines(keepends=True)[:-1],
        text.splitlines(keepends=True)[-1] if text.splitlines(keepends=True) else "",
    ] if "\n" in text else [text]


def _to_source_lines(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if text and not text.endswith("\n"):
        if lines:
            lines[-1] = lines[-1].rstrip("\n")
        else:
            lines = [text]
    return lines or [""]


def _patch_text(src: str, *, langchain_lab: bool) -> tuple[str, bool]:
    original = src

    replacements = [
        ('WATSONX_* from `start_jupyter.ps1`', "OpenAI (`OPENAI_*`) via `watson_llm` from `start_jupyter.ps1`"),
        ("`WATSONX_*` from `start_jupyter.ps1`", "`OPENAI_*` from `start_jupyter.ps1` (via `watson_llm` shim)"),
        ('**`WATSONX_*`** from `start_jupyter.ps1`', "**`OPENAI_*`** from `start_jupyter.ps1` (via `watson_llm` shim)"),
        ('# LOCAL SETUP — llm_model() from WATSONX_* env', "# LOCAL SETUP — OpenAI via watson_llm shim"),
        ('# LOCAL SETUP — ModelInference from WATSONX_* env', "# LOCAL SETUP — OpenAI via watson_helper shim"),
        ("# LOCAL — llm from WATSONX_* env", "# LOCAL — OpenAI via watson_llm shim"),
        ("# LOCAL: compare temperature on WATSONX_MODEL_ID", "# LOCAL: compare temperature on OPENAI_MODEL"),
        ("# LOCAL: WatsonxEmbeddings from WATSONX_* env", "# LOCAL: OpenAI embeddings via make_watsonx_embeddings"),
        ("# LOCAL: WATSONX_* env (name kept for later cells)", "# LOCAL: OpenAI via watson_llm shim"),
        ('print("Model:", __import__("os").environ["WATSONX_MODEL_ID"])', MODEL_PRINT),
        ('print("Model:", os.environ["WATSONX_MODEL_ID"])', 'print("Model:", os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))'),
        ("> **Local:** Compare **temperature 0.8 vs 0.1** on your `WATSONX_MODEL_ID`.",
         "> **Local:** Compare **temperature 0.8 vs 0.1** on your `OPENAI_MODEL`."),
        ("read **`WATSONX_MODEL_ID`**, **`WATSONX_URL`**, **`WATSONX_PROJECT_ID`**, **`WATSONX_APIKEY`**.",
         "use **`OPENAI_API_KEY`**, **`OPENAI_MODEL`**, **`OPENAI_EMBEDDING_MODEL`** (stealth `make_watsonx_*` names)."),
        ("Helpers **`watson_helper.py`** (IBM) and **`watson_llm.py`** (LangChain + embeddings)",
         "Helpers **`watson_helper.py`** and **`watson_llm.py`** (OpenAI backend)"),
        ('project_id=os.environ["WATSONX_PROJECT_ID"]', "# project_id not needed — OpenAI via watson_llm"),
        ('project_id = "skills-network"', "# skills-network skipped — use make_watsonx_llm()"),
    ]
    for old, new in replacements:
        src = src.replace(old, new)

    if HINT_LLM_BLOCK_RE.search(src):
        src = HINT_LLM_BLOCK_RE.sub(HINT_LLM_REPLACEMENT, src)

    if 'llm = WatsonxLLM(' in src and "make_watsonx_llm" not in src:
        src = re.sub(
            r"project_id\s*=\s*[\"']skills-network[\"']\s*\n\s*"
            r"llm = WatsonxLLM\([^)]*\)",
            "from watson_llm import make_watsonx_llm\nllm = make_watsonx_llm(parameters)",
            src,
            flags=re.DOTALL,
        )

    if langchain_lab and "### Running Locally" in src and "OpenAI" not in src:
        src = re.sub(
            r"### Running Locally\n.*?(?=\n###|\n##|\Z)",
            LOCAL_RUNNING_MD + "\n",
            src,
            count=1,
            flags=re.DOTALL,
        )

    src = _strip_ibm_runtime_imports(src)

    return src, src != original


def _insert_local_note(nb: dict, note: str, overview_idx: int) -> bool:
    overview = "".join(nb["cells"][overview_idx].get("source", []))
    if note.strip() in overview or "PROVIDER_SWAP_WATSON_TO_OPENAI" in overview:
        return False
    nb["cells"][overview_idx]["source"] = [note, *nb["cells"][overview_idx].get("source", [])]
    return True


def patch_notebook(path: Path) -> dict[str, int]:
    nb = json.loads(path.read_text(encoding="utf-8"))
    langchain_lab = path.name == "sean_langchain_lab.ipynb"
    stats = {"cells": 0, "overview": 0, "outputs_cleared": 0}

    note = LANGCHAIN_LOCAL_NOTE if langchain_lab else IN_CONTEXT_LOCAL_NOTE
    overview_idx = 4 if langchain_lab else 3
    if _insert_local_note(nb, note, overview_idx):
        stats["overview"] += 1

    for cell in nb["cells"]:
        src = "".join(cell.get("source", []))
        patched, changed = _patch_text(src, langchain_lab=langchain_lab)
        if changed:
            cell["source"] = _to_source_lines(patched)
            stats["cells"] += 1
            if cell.get("cell_type") == "code":
                cell["outputs"] = []
                cell["execution_count"] = None

        if cell.get("cell_type") == "code":
            out_text = json.dumps(cell.get("outputs", []))
            if "WatsonxLLM(" in out_text or "watsonx_model" in out_text:
                cell["outputs"] = []
                cell["execution_count"] = None
                stats["outputs_cleared"] += 1

    path.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    return stats


def main() -> None:
    for path in NOTEBOOKS:
        if not path.exists():
            print("SKIP (missing):", path.name)
            continue
        stats = patch_notebook(path)
        print(f"Patched: {path.name}")
        print(f"  cells changed: {stats['cells']}")
        print(f"  overview: {stats['overview']}")
        print(f"  stale outputs cleared: {stats['outputs_cleared']}")


if __name__ == "__main__":
    main()