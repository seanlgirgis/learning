# Capstone 01 — Course Notes RAG Tutor

← [All capstones](capstones.md)

**Two scripts** — same idea as real apps: **prepare once (many docs over time)**, **chat many times**.

| Script | Job | When you run it |
|--------|-----|-----------------|
| **`capstone_01_ingest.py`** | **Consume** PDF (local or URL) → chunk → embed → **append to Chroma** | Per document (dedupe skips unchanged) |
| **`capstone_01_chat.py`** | **Open saved Chroma** → answer your questions | Whenever you want to ask |

---

## Story (layman)

**Script A (ingest):** Librarian scans each PDF once, stamps it in a ledger (`ingest_manifest.json`), files index cards in a cabinet (Chroma). Same PDF twice? Ledger says “already filed” — skip.

**Script B (chat):** You ask across **all** filed docs — librarian pulls the best cards from any source, Watson answers.

---

## Recommended corpus (build a real RAG knowledge base)

The LangChain course paper alone is **high-level**. Layer these PDFs (listed in **`corpus_sources.json`**):

| Tier | Document | Why add it |
|------|----------|------------|
| **1** | LangChain paper (course URL) | Your lab anchor — components, chains, agents |
| **1** | [RAG paper](https://arxiv.org/pdf/2005.11401.pdf) (Lewis et al.) | Original RAG definition — retriever + generator |
| **2** | [DPR paper](https://arxiv.org/pdf/2004.04906.pdf) | Why **dense embeddings** beat keyword search |
| **2** | [Lost in the Middle](https://arxiv.org/pdf/2307.03172.pdf) | Chunk order + context limits — why `k` and splitting matter |

**Phase 2 (later bite):** HTML from LangChain docs (`WebBaseLoader`) — URLs in `corpus_sources.json` → `web_phase2`.

**Your own PDFs:** Save under `capstone/data/pdfs/` and ingest by path.

```powershell
python .\capstone\capstone_01_ingest.py --corpus          # tier 1+2 PDFs, skip dupes
python .\capstone\capstone_01_ingest.py --list            # what is already in the DB
python .\capstone\capstone_01_ingest.py <path-or-url>     # one document
python .\capstone\capstone_01_ingest.py --force <source>  # re-embed even if unchanged
```

---

## What lab ideas this rolls up

| Idea | Script | Labs |
|------|--------|------|
| Load + split | ingest | 23–27 |
| Embed + Chroma (persist + append) | ingest | 28–29 |
| Retriever + RetrievalQA | chat | 30–31 |

**Modules:** [12](../../../reference/langchain/modules/12-document-loaders.html)–[16](../../../reference/langchain/modules/16-retrievers-rag.html) · [RAG guide](../../../reference/langchain/guides/rag-pipeline.html)

---

## Shared constants (both scripts must match)

```text
capstone/data/chroma_01/          ← persisted vector store
capstone/data/ingest_manifest.json ← dedupe ledger (source + content hash)
```

Same `CHUNK_SIZE` / `CHUNK_OVERLAP`, same `make_watsonx_embeddings` params in **both** files.

**Dedupe rule:** SHA-256 of PDF bytes + normalized source id. Unchanged file → skip. Changed file → delete old chunks for that source, re-embed.

---

## Script A — `capstone_01_ingest.py` (you type this)

**Parallel notebook:** `playground/notebooks/sean_capstone01_ingest_lab.ipynb` — try each bite in a cell first.

**Answer key (after you try):** `capstone_01_ingest_reference.py` — do not peek first.

**Pipeline:** resolve source → hash → skip or load → split → tag metadata → embed → add to Chroma

| Bite | You build |
|------|-----------|
| 1 | Imports + paths (`CHROMA_DIR`, `MANIFEST_PATH`) + chunk constants |
| 2 | `is_url` / `normalize_source` / `read_pdf_bytes` + `sha256_bytes` |
| 3 | `load_manifest` / `save_manifest` + skip-if-unchanged logic |
| 4 | `PyPDFLoader` + splitter → chunks with `ingest_source_id` metadata |
| 5 | Open or create Chroma · `add_documents` · delete stale source on update |
| 6 | `argparse`: positional source, `--list`, `--corpus`, `--force` |

```powershell
python .\capstone\capstone_01_ingest.py
python .\capstone\capstone_01_ingest.py https://arxiv.org/pdf/2005.11401.pdf
```

Needs **network** (URL fetch + embeddings).

---

## Script B — `capstone_01_chat.py` (Q&A)

**Pipeline:** open Chroma from disk → retriever → RetrievalQA → question loop

| Bite | You build |
|------|-----------|
| 1 | Imports + `CHROMA_DIR` (same path as ingest) |
| 2 | Check folder exists — friendly error if ingest not run |
| 3 | `Chroma(persist_directory=..., embedding_function=...)` — **load**, not from_documents |
| 4 | `as_retriever(k=3)` + `RetrievalQA` + `make_watsonx_llm()` |
| 5 | `main`: one-shot (`sys.argv`) **or** `input()` loop until `quit` |

```powershell
python .\capstone\capstone_01_chat.py "What is retrieval augmented generation?"
python .\capstone\capstone_01_chat.py "How does LangChain differ from the original RAG paper?"
```

Needs **network** (Watsonx LLM). Chroma is local after ingest.

---

## Run order

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\playground\langchain

python .\capstone\capstone_01_ingest.py --corpus
python .\capstone\capstone_01_ingest.py --list
python .\capstone\capstone_01_chat.py "What is dense passage retrieval?"
```

---

## Traps

| Symptom | Fix |
|---------|-----|
| Chat says no DB | Run **ingest** first |
| Empty answers | Run `--list`; ingest more tier-1 PDFs |
| Re-ingest every time | Check manifest — same hash should **skip** |
| Different embedding model between scripts | Same `make_watsonx_embeddings` params in A and B |
| `RetrievalQA` import | `langchain_classic.chains` |

---

## Stretch

- Chat: `return_source_documents=True` — print `ingest_title` / page
- Ingest: `WebBaseLoader` branch for `web_phase2` URLs
- Ingest: `--dry-run` (hash + chunk count only, no embed)

---

## Done when

- [ ] `--corpus` loads ≥2 tier-1 PDFs; `--list` shows both
- [ ] Re-run same URL → **Skip (unchanged)**
- [ ] Chat answers cross-document questions
- [ ] You can explain **ingest vs chat** and **dedupe** in one sentence each

---

## Session

**Ingest first:** open notebook OR say **ingest bite 1** → type `capstone_01_ingest.py`  
**Then chat:** say **chat bite 1** → type `capstone_01_chat.py`

← [capstones.md](capstones.md)