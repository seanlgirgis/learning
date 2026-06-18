"""One-shot: notebooks + langchain labs → watson_helper + watson_llm only."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGCHAIN = ROOT.parent / "langchain"

REPLACEMENTS = [
    ("from coursera_watsonx_model import", "from watson_helper import"),
    ("Loaded coursera_watsonx_model.py", "Loaded watson_helper.py"),
    ("coursera_watsonx_model.py", "watson_helper.py"),
    ("from coursera_llm_model import llm_model, make_llm", "from watson_llm import llm_model, make_watsonx_llm"),
    ("from coursera_llm_model import make_llm", "from watson_llm import make_watsonx_llm"),
    ("importlib.reload(coursera_llm_model)", "importlib.reload(watson_llm)"),
    ("import importlib, coursera_llm_model", "import importlib, watson_llm"),
    ("Loaded coursera_llm_model.py", "Loaded watson_llm.py"),
    ("coursera_llm_model.py", "watson_llm.py"),
    ("from coursera_embeddings import make_embeddings", "from watson_llm import make_watsonx_embeddings"),
    ("make_embeddings(", "make_watsonx_embeddings("),
    ("from langchain_helper import make_llm, GenParams", "from watson_llm import GenParams, make_watsonx_llm"),
    ("from langchain_helper import make_llm", "from watson_llm import make_watsonx_llm"),
    ("make_llm(", "make_watsonx_llm("),
    ("langchain_helper", "watson_llm"),
    ("Helpers `watson_llm.py`, `watson_llm.py`, and `watson_llm.py`", "Helpers `watson_helper.py` and `watson_llm.py`"),
    (
        "Helpers `watson_helper.py`, `watson_llm.py`, and `coursera_embeddings.py`",
        "Helpers `watson_helper.py` (IBM) and `watson_llm.py` (LangChain + embeddings)",
    ),
    (
        "This copy uses **`start_jupyter.ps1`** (runs `set_env.ps1`). Helpers `coursera_watsonx_model.py`, `coursera_llm_model.py`, and `coursera_embeddings.py`",
        "This copy uses **`start_jupyter.ps1`** (runs `set_env.ps1` + adds `playground/langchain` to PYTHONPATH). Helpers **`watson_helper.py`** and **`watson_llm.py`**",
    ),
    ("# from coursera_watsonx_model", "# from watson_helper"),
]


def apply(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def migrate_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = apply(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def migrate_notebook(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for cell in data.get("cells", []):
        if cell.get("cell_type") in ("code", "markdown"):
            src = cell.get("source", [])
            if isinstance(src, list):
                joined = "".join(src)
                new_joined = apply(joined)
                if new_joined != joined:
                    cell["source"] = [line for line in new_joined.splitlines(keepends=True)]
                    if cell["source"] and not cell["source"][-1].endswith("\n"):
                        pass
                    changed = True
            elif isinstance(src, str):
                new_src = apply(src)
                if new_src != src:
                    cell["source"] = new_src
                    changed = True
    if changed:
        path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    touched: list[str] = []

    for py in LANGCHAIN.glob("*.py"):
        if py.name in ("migrate_two_helpers.py",):
            continue
        if migrate_file(py):
            touched.append(str(py.relative_to(ROOT.parent.parent)))

    for name in ("prepare_local_notebooks.py", "patch_langchain_env.py", "README.md"):
        p = ROOT / name
        if p.exists() and migrate_file(p):
            touched.append(str(p.relative_to(ROOT.parent.parent)))

    for nb in ROOT.glob("*.ipynb"):
        if migrate_notebook(nb):
            touched.append(str(nb.relative_to(ROOT.parent.parent)))

    print("Updated files:")
    for t in touched:
        print(" ", t)


if __name__ == "__main__":
    main()