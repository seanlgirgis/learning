# Notebooks

**Your working copies** of the two crs_001 Coursera labs — patched for local `WATSONX_*` env.

| File | Source |
|------|--------|
| `sean_in_context_lab.ipynb` | In-Context Learning and Prompt Templates |
| `sean_langchain_lab.ipynb` | Build Smarter AI Apps / LangChain |

Pristine downloads stay in `Downloads\Coursera_lab\AI0220EN` and
`courses/.../source_material/`.

## One-time install (foundation venv)

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
pip install -r D:\Workarea\learning\playground\notebooks\requirements-jupyter.txt
python -m ipykernel install --user --name rag_foundation --display-name "RAG Foundation (Python 3.13)"
```

## Start Jupyter Lab (port **8892** — not Docker’s 8888)

```powershell
D:\Workarea\learning\playground\notebooks\start_jupyter.ps1
```

Custom port:

```powershell
.\start_jupyter.ps1 -Port 8895
```

## Local env helpers (imported by patched notebooks)

| Module | Used by |
|--------|---------|
| `coursera_llm_model.py` | In-Context lab — `make_llm()` and `llm_model()` |
| `coursera_watsonx_model.py` | LangChain lab — `model` (ModelInference), `credentials` |
| `coursera_embeddings.py` | LangChain lab — `make_embeddings()` for RAG cells |

Both read **`WATSONX_MODEL_ID`**, **`WATSONX_URL`**, **`WATSONX_PROJECT_ID`**, **`WATSONX_APIKEY`** from `set_env.ps1`.

## Refresh notebooks from Downloads

After you pull a newer cache from Coursera:

```powershell
python D:\Workarea\learning\playground\notebooks\prepare_local_notebooks.py
```

Re-apply env patches only (without re-copying from Downloads):

```powershell
python D:\Workarea\learning\playground\notebooks\patch_langchain_env.py
```

## Import note (LangChain 1.x venv)

Coursera pins 0.2.x. Patched In-Context copy uses `langchain_classic` for `LLMChain`.
Full table: `../langchain/coursera_import_map.md`.

## Suggested workflow

1. **Learn** — bite-sized `.py` in `../langchain/` (e.g. `08.lcel.1.py`).
2. **Reference** — run notebook sections when a cell confuses you.
3. **Grade on Coursera** — IBM Skills Network lab when an exercise must be submitted.