"""Patch sean_langchain_lab.ipynb to use WATSONX_* env instead of Skills Network."""

from __future__ import annotations

import json
import re
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parent / "sean_langchain_lab.ipynb"

LOCAL_NOTE = (
    "> **Local copy:** LLM + embeddings via **`watson_llm`** / **`watson_helper`** → **OpenAI** "
    "(`OPENAI_*` from `start_jupyter.ps1`). Not `skills-network` or Coursera demo models.\n\n"
)

LOCAL_MODEL_CELL = """# LOCAL SETUP — OpenAI via watson_helper shim
from watson_helper import credentials, model, model_id, parameters, project_id

print("Loaded watson_helper.py")
print("Model:", model_id)
print("URL:", credentials["url"])
"""

LOCAL_RUNNING_MD = (
    "### Running Locally\n\n"
    "This copy uses **`start_jupyter.ps1`** (runs `set_env.ps1`). "
    "Helpers **`watson_helper.py`** and **`watson_llm.py`** in `../langchain/` call **OpenAI** "
    "via `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL` (stealth `make_watsonx_*` names).\n"
)

LOCAL_MODEL_MD = (
    "The following cell loads your watsonx model from environment variables "
    "(not Coursera's `ibm/granite-4-h-small` demo):\n"
)

CHAT_LLM_CELL = """from watson_llm import make_watsonx_llm

llama_llm = make_watsonx_llm()  # LOCAL: OpenAI via watson_llm shim
"""

EMBEDDING_CELL = """# LOCAL: OpenAI embeddings via make_watsonx_embeddings
from watson_llm import make_watsonx_embeddings

watsonx_embedding = make_watsonx_embeddings(embed_params)
"""

EXERCISE_1_STARTER = """# LOCAL: compare temperature on OPENAI_MODEL
# (Coursera compares Granite vs Llama on Skills Network)
from watson_llm import make_watsonx_llm
import os

print("Model:", os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))

parameters_creative = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.8,
}

parameters_precise = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.1,
}

llm_creative = make_watsonx_llm(parameters_creative)
llm_precise = make_watsonx_llm(parameters_precise)

prompts = [
    "Write a short poem about artificial intelligence",
    "What are the key components of a neural network?",
    "List 5 tips for effective time management",
]

# TODO: Send identical prompts to llm_creative and llm_precise; compare outputs.
"""

EXERCISE_1_SOLUTION = """# LOCAL: same model, two temperatures
from watson_llm import make_watsonx_llm
import os

print("Model:", os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))

parameters_creative = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.8,
}

parameters_precise = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.1,
}

llm_creative = make_watsonx_llm(parameters_creative)
llm_precise = make_watsonx_llm(parameters_precise)

prompts = [
    "Write a short poem about artificial intelligence",
    "What are the key components of a neural network?",
    "List 5 tips for effective time management",
]

for prompt in prompts:
    print(f"\\n\\nPrompt: {prompt}")
    print("\\nCreative response (Temperature = 0.8):")
    print(llm_creative.invoke(prompt))
    print("\\nPrecise response (Temperature = 0.1):")
    print(llm_precise.invoke(prompt))
"""

EXERCISE_1_MD_NOTE = (
    "> **Local:** Compare **temperature 0.8 vs 0.1** on your `OPENAI_MODEL`. "
    "Coursera's Skills Network lab compares Granite vs Llama — skip that here.\n\n"
)

OLD_WATSONX_LLM_IMPORT = (
    "from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM"
)
LOCAL_WATSONX_LLM_IMPORT = (
    "from watson_llm import make_watsonx_llm  # local: OpenAI shim (not langchain_ibm)"
)

WATSONX_EMBEDDINGS_RE = re.compile(
    r"(?:watsonx_embedding|embedding_model)\s*=\s*WatsonxEmbeddings\(\s*"
    r'model_id="ibm/slate-125m-english-rtrvr-v2",\s*'
    r'url="https://us-south\.ml\.cloud\.ibm\.com",\s*'
    r'project_id="skills-network",\s*'
    r"params=embed_params,\s*\)",
    re.MULTILINE,
)

EXERCISE_5_MODEL_BLOCK_RE = re.compile(
    r"model_id\s*=\s*['\"]meta-llama/llama-4-maverick.*?"
    r"llm\s*=\s*WatsonxLLM\(model=model\)",
    re.DOTALL,
)

EXERCISE_5_MAKE_LLM = """from watson_llm import make_watsonx_llm

parameters = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.2,
}
llm = make_watsonx_llm(parameters)"""

LANGCHAIN_CHAIN_IMPORTS = (
    ("from langchain.chains import LLMChain, SequentialChain", "from langchain_classic.chains import LLMChain, SequentialChain"),
    ("from langchain.chains import ConversationChain", "from langchain_classic.chains import ConversationChain"),
    ("from langchain.chains import RetrievalQA", "from langchain_classic.chains import RetrievalQA"),
    ("from langchain.chains import LLMChain", "from langchain_classic.chains import LLMChain"),
)


def _splitlines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def _patch_imports(src: str) -> str:
    for old, new in LANGCHAIN_CHAIN_IMPORTS:
        src = src.replace(old, new)
    src = src.replace(OLD_WATSONX_LLM_IMPORT, LOCAL_WATSONX_LLM_IMPORT)
    return src


def _ensure_embedding_import(src: str) -> str:
    if "make_watsonx_embeddings" in src and "from watson_llm import make_watsonx_embeddings" not in src:
        src = "from watson_llm import make_watsonx_embeddings\n" + src
    return src


def _patch_embeddings(src: str) -> str:
    if WATSONX_EMBEDDINGS_RE.search(src):
        src = WATSONX_EMBEDDINGS_RE.sub("embedding_model = make_watsonx_embeddings(embed_params)", src)
        src = src.replace(
            "embedding_model = make_watsonx_embeddings(embed_params)",
            "watsonx_embedding = make_watsonx_embeddings(embed_params)",
            1,
        ) if "watsonx_embedding = WatsonxEmbeddings" in src else src
        # fix double replacement: handle watsonx_embedding vs embedding_model separately
    if 'watsonx_embedding = WatsonxEmbeddings' in src or (
        'embedding_model = WatsonxEmbeddings' in src and "skills-network" in src
    ):
        # full cell replacement for demo cell pattern
        if "embed_params" in src and "EmbedTextParamsMetaNames" not in src:
            pass
    return src


def _patch_cell(src: str, cell_type: str) -> tuple[str, bool]:
    original = src
    src = _patch_imports(src)

    if cell_type == "code":
        if src.strip() == "llama_llm = WatsonxLLM(model = model)":
            src = CHAT_LLM_CELL

        if "granite='ibm/granite-4-h-small'" in src and "# TODO:" in src:
            src = EXERCISE_1_STARTER

        if "watsonx_embedding = WatsonxEmbeddings" in src and "skills-network" in src:
            src = EMBEDDING_CELL

        if "embedding_model = ##TODO: use ibm/slate-125m-english-rtrvr-v2" in src:
            src = src.replace(
                "embedding_model = ##TODO: use ibm/slate-125m-english-rtrvr-v2 model\n)",
                "embedding_model = make_watsonx_embeddings(embed_params)",
            )
            src = _ensure_embedding_import(src)

        if 'credentials = {"url": "https://us-south.ml.cloud.ibm.com"}' in src:
            src = src.replace(
                'credentials = {"url": "https://us-south.ml.cloud.ibm.com"}\n\n',
                "",
            )
            src = src.replace(
                'credentials = {"url": "https://us-south.ml.cloud.ibm.com"}\n',
                "",
            )

        if re.search(r"model\s*=\s*##TODO", src) and "make_llm" in src:
            src = re.sub(r"\n# Initialize the model\nmodel = ##TODO\n", "\n", src)
            src = re.sub(r"model = ##TODO\n", "", src)

        if "llm = make_watsonx_llm(parameters)" in src and "ConversationChain" in src:
            drop = (
                "from ibm_watsonx_ai.foundation_models import ModelInference\n",
                "from langchain_ibm import WatsonxLLM  # local: not ibm_watson_machine_learning (Py 3.13)\n",
                "from langchain_ibm import WatsonxLLM\n",
            )
            for line in drop:
                src = src.replace(line, "")
            if "from watson_llm import make_watsonx_llm" not in src:
                src = "from watson_llm import make_watsonx_llm\n" + src

    if cell_type == "markdown":
        if "### Running Locally" in src and "start_jupyter.ps1" not in src:
            src = re.sub(
                r"### Running Locally\n.*?(?=\n###|\n##|\Z)",
                LOCAL_RUNNING_MD + "\n",
                src,
                count=1,
                flags=re.DOTALL,
            )

        if "construct a `ibm/granite-4-h-small`" in src:
            src = LOCAL_MODEL_MD

        if "### Exercise 1" in src and "Compare Model Responses" in src:
            if EXERCISE_1_MD_NOTE.strip() not in src:
                src = EXERCISE_1_MD_NOTE + src

        if "<summary>Click here for the solution</summary>" in src and "granite_creative = ModelInference" in src:
            src = re.sub(
                r"```python\n.*?```",
                f"```python\n{EXERCISE_1_SOLUTION}\n```",
                src,
                count=1,
                flags=re.DOTALL,
            )

        if EXERCISE_5_MODEL_BLOCK_RE.search(src):
            src = EXERCISE_5_MODEL_BLOCK_RE.sub(EXERCISE_5_MAKE_LLM, src)

        if "embedding_model = WatsonxEmbeddings" in src and "skills-network" in src:
            block = (
                "embedding_model = make_watsonx_embeddings(embed_params)"
            )
            src = WATSONX_EMBEDDINGS_RE.sub(block, src)
            if "from watson_llm import make_watsonx_embeddings" not in src:
                src = src.replace(
                    "```python\n",
                    "```python\nfrom watson_llm import make_watsonx_embeddings\n",
                    1,
                )

    # generic embedding blocks in any cell
    if "skills-network" in src and "WatsonxEmbeddings" in src:
        var = "watsonx_embedding" if "watsonx_embedding" in src else "embedding_model"
        src = WATSONX_EMBEDDINGS_RE.sub(f"{var} = make_watsonx_embeddings(embed_params)", src)
        src = _ensure_embedding_import(src)

    src = src.replace('project_id = "skills-network"', "project_id = project_id  # from watson_helper")
    src = src.replace("project_id=\"skills-network\"", "# skills-network skipped — use make_watsonx_llm()")

    return src, src != original


def patch_langchain_notebook(nb: dict) -> dict[str, int]:
    stats = {"cells": 0, "overview": 0, "local_setup": 0}

    title = nb["cells"][1].get("source", [])
    if title and "LOCAL" not in title[0] and "local copy" not in title[0].lower():
        title[0] = title[0].rstrip() + " (local copy — Sean)\n"
        stats["overview"] += 1

    overview = "".join(nb["cells"][4].get("source", []))
    if LOCAL_NOTE not in overview:
        nb["cells"][4]["source"] = [LOCAL_NOTE, *nb["cells"][4].get("source", [])]
        stats["overview"] += 1

    nb["cells"][24]["source"] = _splitlines(LOCAL_MODEL_CELL)
    nb["cells"][24]["outputs"] = []
    nb["cells"][24]["execution_count"] = None
    stats["local_setup"] += 1

    for cell in nb["cells"]:
        src = "".join(cell.get("source", []))
        patched, changed = _patch_cell(src, cell["cell_type"])
        if changed:
            cell["source"] = _splitlines(patched)
            if cell["cell_type"] == "code":
                cell["outputs"] = []
                cell["execution_count"] = None
            stats["cells"] += 1

    return stats


def main() -> None:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    stats = patch_langchain_notebook(nb)
    NOTEBOOK.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print("Patched:", NOTEBOOK.name)
    print("  cells changed:", stats["cells"])
    print("  overview:", stats["overview"])
    print("  local setup:", stats["local_setup"])


if __name__ == "__main__":
    main()