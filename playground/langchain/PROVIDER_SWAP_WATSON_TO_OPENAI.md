# Provider swap: IBM watsonx → OpenAI (stealth shim)

**Date:** 2026-06-19  
**Reason:** IBM learning / generation quota exhausted (`token_quota_reached`). Capstones and playground labs must keep running without rewriting every script.

**Strategy:** Keep **watsonx-compatible function and file names** (`make_watsonx_llm`, `watson_llm.py`, `GenParams`, etc.). Implementations call **OpenAI** via `langchain_openai`. No IBM API calls at runtime for LLM or embeddings.

**Future:** Add a second provider (e.g. Grok) behind the same helpers with `LLM_PROVIDER` in `set_env.ps1`.

---

## Environment (`set_env.ps1`)

Location: `D:\py_venv\rag_application_builder_foundation\set_env.ps1` (outside this git repo).

| Variable | Role |
|----------|------|
| `OPENAI_API_KEY` | Required for all LLM + embedding calls |
| `OPENAI_MODEL` | Chat model (e.g. `gpt-5.4-mini`) |
| `OPENAI_EMBEDDING_MODEL` | Embeddings (default `text-embedding-3-small`) |

`WATSONX_*` vars may still be set but are **not used** by the shimmed helpers.

---

## Files directly changed

### Core shims (the whole swap lives here)

| File | Change |
|------|--------|
| **`watson_llm.py`** | Rewritten. `make_watsonx_llm` / `make_watsonx_chat` → `ChatOpenAI`. `make_watsonx_embeddings` → `OpenAIEmbeddings`. `llm_model()` → OpenAI. `GenParams` / `EmbedTextParamsMetaNames` still imported for lab param dicts; IBM-only keys ignored for embeddings. `missing_watsonx_env()` delegates to `missing_openai_env()`. |
| **`watson_helper.py`** | Rewritten. Lab 15 `ModelInference.generate()` shape preserved; backend is OpenAI via `make_watsonx_llm`. `model_id` = `OPENAI_MODEL`, `credentials["url"]` = `https://api.openai.com/v1`. |

### Playground wiring

| File | Change |
|------|--------|
| **`00_env_check.py`** | Checks `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL` only. Notes stealth swap. |
| **`08.lcel.1.py`** | Removed direct `langchain_ibm.WatsonxLLM`; uses `make_watsonx_llm()`. |
| **`09.LCEL.Summurization.py`** | Same |
| **`10.lcelanswer.py`** | Same |
| **`11.lcel.classification.py`** | Same |
| **`12.lcel.generatesql.py`** | Same |
| **`13.lcel.bot.py`** | Same |
| **`14.lcel.chain.custom_formatting.py`** | Same |
| **`16.watson_llm.invoke_test.py`** | Prints `OPENAI_MODEL` instead of `WATSONX_MODEL_ID`. |
| **`18.temperature.compare.py`** | Prints `OPENAI_MODEL` instead of `WATSONX_MODEL_ID`. |

### Capstone 01 (RAG)

| File | Change |
|------|--------|
| **`capstone/capstone_shared.py`** | `CHROMA_DIR` → `data/chroma_01_openai` (avoid mixing old Watson vectors with OpenAI). Removed IBM-only `EMBED_PARAMS`. `make_embedding_model()` calls `make_watsonx_embeddings()` with no IBM params. |

**Action required:** Re-run `capstone_01_ingest.py` once so Chroma is built with OpenAI embeddings.

---

## Files covered indirectly (no edit needed)

These import `watson_llm` / `watson_helper` and **automatically use OpenAI** after the shim:

### LLM via `make_watsonx_llm` or `llm_model`

| Script | Notes |
|--------|--------|
| `02_watson_llm.py` | Examples |
| `03_example1_format_oneShot.py` | |
| `04.Fewshotexample.py` | |
| `05.cot.py` | |
| `06.cot.2tests.py` | |
| `07.self_consistency.py` | |
| `14b.runnable_lambda.practical.py` | |
| `17.chat_messages.invoke_test.py` | |
| `19.params.py` | |
| `20.chat_prompt_templates.py` | |
| `21.output_parsers.py` | |
| `22.exercise2.movie_json.py` | |
| `33.memory.py` | |
| `34.chains.py` | |
| `35.agents.py` | |
| `try_lcel_pipe.py` | |
| `lcel_pipe.py` | |
| `drill_llm_model_local.py` | |
| `try_import_watson_llm.py` | |
| `capstone/capstone_01_chat.py` | |
| `capstone/capstone_02_review_desk.py` | |
| `capstone/capstone_03_remember_me_chat.py` | |
| `capstone/capstone_03_remember_me_chat_bare.py` | |

### Embeddings via `make_watsonx_embeddings`

| Script | Notes |
|--------|--------|
| `28.embeddings.demo.py` | Still passes IBM `embed_params`; ignored by shim |
| `29.chroma.store_search.py` | |
| `30.exercise.retriever.py` | |
| `31.rag.retrieval_qa.py` | |
| `32.parent_document_retriever.py` | |

### Lab 15 helper

| Script | Notes |
|--------|--------|
| `15.watson_helper.generate_test.py` | Uses `watson_helper.model.generate()` |

### No LLM / no embeddings (unaffected)

| Script | Notes |
|--------|--------|
| `23.document.object.py` | Documents only |
| `24.loader.pdf.py` | Loaders |
| `25.loader.web.py` | |
| `26.splitter.character.py` | Splitters |
| `27.exercise3.load_split.py` | |
| `capstone/debug_retrieval.py` | Uses Chroma + capstone_shared |

---

## Playground coverage summary

| Area | Count | Status |
|------|-------|--------|
| Labs **00–35** under `playground/langchain/` | 36 numbered scripts + helpers | **Runtime covered** — all network LLM/embedding paths go through shims |
| **Capstones 01–03** | 6 scripts + `capstone_shared` | **Covered** — 01 needs re-ingest |
| Direct `langchain_ibm.WatsonxLLM` in playground | Was 7 LCEL files | **Fixed** (08–14) |

---

## Smoke tests run (2026-06-19)

| Test | Result |
|------|--------|
| `00_env_check.py` | OK |
| `28.embeddings.demo.py` | 3 vectors × 1536 dims |
| `15.watson_helper.generate_test.py` | OK (chat-style continuation vs old completion — behavior differs slightly) |
| `16.watson_llm.invoke_test.py` | OK |
| `08.lcel.1.py` | LCEL pipe OK |
| `capstone_02` `analyze_review()` | 3-step chain OK |

---

## Not covered (still mention watsonx or call IBM directly)

These are **outside** the stealth shim path. They do not break the playground, but they are not swapped.

| Location | What | Risk |
|----------|------|------|
| **`courses/crs_001_.../lab/python/05c_lcel_watsonx_pipeline.py`** | Direct `ChatWatsonx` | Fails without Watson quota |
| **`courses/crs_001_.../lab/python/05d_watsonx_smallest_test.py`** | Direct `ChatWatsonx` | Same |
| **`courses/crs_001_.../lab/python/05f_provider_switching_lcel_pipeline.py`** | Direct `ChatWatsonx` | Same |
| **`playground/notebooks/sean_in_context_lab.ipynb`** | Patched 2026-06-19 — OpenAI banners + setup cells | Run `patch_notebooks_openai.py` after Coursera refresh |
| **`playground/notebooks/sean_langchain_lab.ipynb`** | Patched 2026-06-19 — same + `patch_langchain_env.py` | Coursera **course text** still mentions IBM; **code cells** use `make_watsonx_*` |
| **`playground/notebooks/sean_capstone01_ingest_lab.ipynb`** | Env check still lists `WATSONX_*` | Embeddings cell uses `make_watsonx_embeddings` (OpenAI) when you uncomment |
| **`01_import_probe.py`** | Still verifies `langchain_ibm` / `ibm_watsonx_ai` **packages install** | Probe passes if packages installed; runtime does not use them |
| **`reference/langchain/modules/02-watsonx-llm.html`** | Course reference HTML | Teaching material, not runtime |
| **Planning / memory markdown** | `GROK_MEMORY.md`, capstone plans, etc. | Docs only |
| **Capstone docstrings** | e.g. `capstone_02` “3 Watsonx LLM calls”, `capstone_01_ingest` “Embed with Watsonx” | Stale wording only |

---

## Behavioral differences (OpenAI vs Watson)

| Topic | Note |
|-------|------|
| **Lab 15** `model.generate("In today's sales meeting, we ")` | Watson completion continued the sentence; OpenAI chat may ask for clarification. API shape unchanged. |
| **Lab 16** `invoke()` | May print full `AIMessage` object instead of plain string (pre-existing display quirk). |
| **Embeddings** | OpenAI `text-embedding-3-small` = 1536 dims vs IBM slate; **must re-embed** Chroma data. |
| **`GenParams.TOP_K`** | Ignored for OpenAI (was Watson-specific). |

---

## How to verify after pull

```powershell
. D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\playground\langchain

python 00_env_check.py
python 28.embeddings.demo.py
python 16.watson_llm.invoke_test.py

cd capstone
python capstone_01_ingest.py   # once, for RAG
python capstone_02_review_desk.py
```

---

## Architecture (one diagram)

```text
  Lab / capstone script
        │
        ├─ make_watsonx_llm()  ──► watson_llm.py ──► ChatOpenAI (OPENAI_*)
        ├─ make_watsonx_embeddings() ──► watson_llm.py ──► OpenAIEmbeddings
        └─ watson_helper.model.generate() ──► watson_helper.py ──► same ChatOpenAI

  Names say "watsonx" · Network calls go to OpenAI only
```

---

## Checklist: are we covered?

- [x] All **playground** scripts that call the network for text generation
- [x] All **playground** scripts that call the network for embeddings (via shim)
- [x] **Capstones 02 & 03** (chains, memory, agents-style LLM)
- [x] **Capstone 01** code path (after one re-ingest to `chroma_01_openai`)
- [x] **Lab 15** IBM SDK-style `generate()`
- [ ] **Coursera course lab folder** `05c` / `05d` / `05f` (separate tree; not shimmed)
- [ ] **Notebook patch scripts / README** (wording still Watson; optional cleanup)
- [ ] **Reference HTML** (optional doc update)
- [ ] **Multi-provider** (Grok) — future `LLM_PROVIDER` branch in `watson_llm.py`