"""Copy Coursera AI0220EN notebooks and patch for local WATSONX_* env."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

SRC = Path(r"D:\Users\shareuser\Downloads\Coursera_lab\AI0220EN")
DST = Path(__file__).resolve().parent

IN_CONTEXT_SRC = SRC / "In-Context Learning and Prompt Templates for Advanced AI.ipynb"
LANGCHAIN_SRC = SRC / "Build Smarter AI Apps Empower LLMs with LangChain.ipynb"

IN_CONTEXT_DST = DST / "sean_in_context_lab.ipynb"
LANGCHAIN_DST = DST / "sean_langchain_lab.ipynb"

LOCAL_NOTE = (
    "> **Local copy:** LLM via **`make_watsonx_llm`** → **OpenAI** (`OPENAI_*` from "
    "`start_jupyter.ps1`). Not `skills-network` or `ibm/granite-4-h-small`.\n"
)

LOCAL_LLM_CELL = """# LOCAL SETUP — OpenAI via watson_llm shim
from watson_llm import llm_model, make_watsonx_llm

print("Loaded watson_llm.py")
print("Model:", __import__("os").environ.get("OPENAI_MODEL", "gpt-4o-mini"))
"""

SKIP_SKILLS_NETWORK = """### Skills Network cell skipped

Use **`from watson_llm import make_watsonx_llm`** instead of
`project_id = "skills-network"`. Start Jupyter via **`start_jupyter.ps1`**.
"""

LOCAL_MODEL_CELL = """# LOCAL SETUP — OpenAI via watson_helper shim
from watson_helper import credentials, model, model_id, parameters, project_id

print("Loaded watson_helper.py")
print("Model:", model_id)
print("URL:", credentials["url"])
"""

SKILLS_MARKERS = ("skills-network", "ibm/granite-4-h-small", "us-south.ml.cloud.ibm.com")


def _extract_parameters_block(source: str) -> str:
    match = re.search(
        r"(parameters(?:_\w+)?\s*=\s*\{.*?\})",
        source,
        flags=re.DOTALL,
    )
    if match:
        return match.group(1)
    return (
        "parameters = {\n"
        "    GenParams.MAX_NEW_TOKENS: 256,\n"
        "    GenParams.TEMPERATURE: 0.5,\n"
        "}"
    )


def _patch_code_cell(source: str) -> str | None:
    if not any(marker in source for marker in SKILLS_MARKERS):
        return None
    if "WatsonxLLM" not in source and "llm = ## TODO" not in source and "llm = ##TODO" not in source:
        if "model_id" in source and "project_id" in source:
            pass
        else:
            return None

    params_block = _extract_parameters_block(source)

    if re.search(r"llm\s*=\s*##\s*TODO", source, flags=re.IGNORECASE):
        lines = source.splitlines()
        out: list[str] = []
        for line in lines:
            stripped = line.strip()
            if re.match(r'model_id\s*=', stripped):
                continue
            if re.match(r"url\s*=", stripped):
                continue
            if re.match(r'project_id\s*=', stripped):
                continue
            if re.match(r"llm\s*=\s*##\s*TODO", stripped, flags=re.IGNORECASE):
                out.append("llm = make_watsonx_llm(parameters)")
                continue
            out.append(line)
        cleaned = "\n".join(out)
        if "from watson_llm import make_watsonx_llm" not in cleaned:
            cleaned = "from watson_llm import make_watsonx_llm\n\n" + cleaned
        return cleaned + "\n"

    if "WatsonxLLM(" in source and "chain" not in source.lower():
        return (
            "# LOCAL — llm from WATSONX_* env\n"
            "from watson_llm import make_watsonx_llm\n\n"
            f"{params_block}\n\n"
            "llm = make_watsonx_llm(parameters)\n"
            "llm\n"
        )

    return None


def _patch_markdown_cell(source: str) -> str | None:
    if "skills-network" not in source and "ibm/granite-4-h-small" not in source:
        return None
    if "```python" not in source:
        return None

    def repl_block(block: str) -> str:
        patched = _patch_code_cell(block)
        return patched if patched else block

    parts = re.split(r"(```python\n|```\n)", source)
    out: list[str] = []
    i = 0
    while i < len(parts):
        out.append(parts[i])
        if i + 2 < len(parts) and parts[i] == "```python\n":
            out.append(repl_block(parts[i + 1]))
            out.append(parts[i + 2])
            i += 3
        else:
            i += 1
    new_source = "".join(out)
    return new_source if new_source != source else None


def _patch_all_skills_cells(nb: dict) -> int:
    count = 0
    for cell in nb["cells"]:
        src = "".join(cell.get("source", []))
        if cell["cell_type"] == "code":
            patched = _patch_code_cell(src)
            if patched:
                cell["source"] = patched.splitlines(keepends=True)
                cell["outputs"] = []
                cell["execution_count"] = None
                count += 1
        elif cell["cell_type"] == "markdown":
            patched = _patch_markdown_cell(src)
            if patched:
                cell["source"] = patched.splitlines(keepends=True)
                count += 1
    return count


def patch_in_context(nb: dict) -> None:
    for cell in nb["cells"]:
        src = "".join(cell.get("source", []))
        if "from langchain.chains import LLMChain" in src:
            cell["source"] = [
                line.replace(
                    "from langchain.chains import LLMChain",
                    "from langchain_classic.chains import LLMChain",
                )
                for line in cell["source"]
            ]

    nb["cells"][27]["cell_type"] = "code"
    nb["cells"][27]["source"] = LOCAL_LLM_CELL.splitlines(keepends=True)
    nb["cells"][27]["outputs"] = []
    nb["cells"][27]["execution_count"] = None

    nb["cells"][29]["cell_type"] = "markdown"
    nb["cells"][29]["source"] = SKIP_SKILLS_NETWORK.splitlines(keepends=True)

    title = nb["cells"][1].get("source", [])
    if title and "LOCAL" not in title[0]:
        title[0] = title[0].rstrip() + " (local copy — Sean)\n"

    if LOCAL_NOTE not in "".join(nb["cells"][3].get("source", [])):
        nb["cells"][3]["source"] = [LOCAL_NOTE, *nb["cells"][3].get("source", [])]

    patched = _patch_all_skills_cells(nb)
    print(f"  In-Context: patched {patched} skills-network/granite cells")


OLD_WATSONX_LLM_IMPORT = (
    "from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM"
)
LOCAL_WATSONX_LLM_IMPORT = (
    "from langchain_ibm import WatsonxLLM  # local: not ibm_watson_machine_learning (Py 3.13)"
)


def _patch_watsonx_llm_imports(nb: dict) -> int:
    count = 0
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell.get("source", []))
        if OLD_WATSONX_LLM_IMPORT not in src:
            continue
        cell["source"] = [
            line.replace(OLD_WATSONX_LLM_IMPORT, LOCAL_WATSONX_LLM_IMPORT)
            for line in cell["source"]
        ]
        count += 1
    return count


def patch_langchain(nb: dict) -> None:
    from patch_langchain_env import patch_langchain_notebook

    stats = patch_langchain_notebook(nb)
    import_patched = _patch_watsonx_llm_imports(nb)
    patched = _patch_all_skills_cells(nb)
    print(
        f"  LangChain: env patch {stats['cells']} cells, "
        f"{import_patched} WatsonxLLM imports, {patched} skills-network cells"
    )


def main() -> None:
    if not IN_CONTEXT_SRC.exists():
        raise FileNotFoundError(IN_CONTEXT_SRC)

    shutil.copy2(IN_CONTEXT_SRC, IN_CONTEXT_DST)
    shutil.copy2(LANGCHAIN_SRC, LANGCHAIN_DST)

    in_nb = json.loads(IN_CONTEXT_DST.read_text(encoding="utf-8"))
    patch_in_context(in_nb)
    IN_CONTEXT_DST.write_text(json.dumps(in_nb, indent=1), encoding="utf-8")

    lc_nb = json.loads(LANGCHAIN_DST.read_text(encoding="utf-8"))
    patch_langchain(lc_nb)
    LANGCHAIN_DST.write_text(json.dumps(lc_nb, indent=1), encoding="utf-8")

    print("Wrote:", IN_CONTEXT_DST.name)
    print("Wrote:", LANGCHAIN_DST.name)


if __name__ == "__main__":
    main()