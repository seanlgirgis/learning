# Capstone 01A — Ingest flow (`capstone_01_ingest.py`)

← [Capstone overview](capstone01.md) · Shared: [`capstone_shared.py`](capstone_shared.py)

**One sentence:** Librarian scans each PDF or web page once, fingerprints it in a ledger, chunks it, embeds it, and files vectors in Chroma — skipping work when nothing changed.

---

## Big picture

```mermaid
flowchart LR
    subgraph inputs [Inputs]
        PDF[PDF path or .pdf URL]
        WEB[Web URL]
        CORPUS[corpus_sources.json]
    end

    subgraph ingest [capstone_01_ingest.py]
        CLI[CLI router]
        HASH[SHA-256 fingerprint]
        MANIFEST[ingest_manifest.json]
        LOAD[Load + split]
        EMBED[Watsonx embed]
        CHROMA[(Chroma chroma_01)]
    end

    PDF --> CLI
    WEB --> CLI
    CORPUS --> CLI
    CLI --> HASH
    HASH --> MANIFEST
    MANIFEST -->|skip or go| LOAD
    LOAD --> EMBED
    EMBED --> CHROMA
    MANIFEST -.->|records source| MANIFEST
```

**Run once (or when corpus changes).** Chat reads the cabinet later — it does not re-ingest.

---

## CLI router — which path runs?

```mermaid
flowchart TD
    START([python capstone_01_ingest.py]) --> PARSE[argparse]

    PARSE --> LIST{--list?}
    LIST -->|yes| CMD_LIST[cmd_list: print manifest]
    LIST -->|no| CORPUS{--corpus?}

    CORPUS -->|yes| CMD_CORPUS[cmd_corpus: each PDF in sources]
    CORPUS -->|no| WEB{--web?}

    WEB -->|yes| CMD_WEB[cmd_web: each URL in web_phase2]
    WEB -->|no| ONE[ingest_source: positional URL/path or DEFAULT_SOURCE]

    CMD_CORPUS --> INGEST[ingest_source per item]
    CMD_WEB --> INGEST
    ONE --> INGEST

    CMD_LIST --> END([done])
    INGEST --> END
```

| Command | What it ingests |
|---------|-----------------|
| `python capstone_01_ingest.py` | Default LangChain course PDF |
| `python capstone_01_ingest.py <url-or-path>` | One PDF or one web page |
| `python capstone_01_ingest.py --corpus` | All PDFs in `corpus_sources.json` → `sources` |
| `python capstone_01_ingest.py --web` | All HTML URLs in `web_phase2` |
| `python capstone_01_ingest.py --list` | Show manifest only (no embed) |
| `--force` (with any ingest) | Re-embed even if hash unchanged |

---

## Core pipeline — `ingest_source()` step by step

This is the heart of Script A. Every CLI path ends here (except `--list`).

```mermaid
flowchart TD
    A([ingest_source source]) --> B[normalize_source → source_id]
    B --> C[read_source_bytes]
    C --> D[sha256_bytes → content_hash]
    D --> E[load_manifest]
    E --> F{prior hash matches<br/>and not --force?}

    F -->|yes| SKIP([return skipped])
    F -->|no| G[load_and_split]
    G --> H[persist_chunks_to_chroma]
    H --> I[update manifest + save_manifest]
    I --> J([return ingested or updated])
```

### Step detail (study order)

| Step | Function | What happens |
|------|----------|--------------|
| 1 | `normalize_source` | URL stays as-is; local path → absolute path |
| 2 | `read_source_bytes` | PDF: bytes + temp file path. Web: HTML bytes for hash |
| 3 | `sha256_bytes` | Fingerprint raw bytes — dedupe key |
| 4 | `load_manifest` | Read ledger from `data/ingest_manifest.json` |
| 5 | Skip check | Same hash + no `--force` → **no embed, no Chroma touch** |
| 6 | `load_and_split` | Documents → chunks (500 chars, 50 overlap) |
| 7 | `persist_chunks_to_chroma` | Embed + write vectors |
| 8 | `save_manifest` | Record title, kind, hash, chunk_count, timestamp |

---

## PDF vs web — loader branch

```mermaid
flowchart TD
    RS[read_source_bytes] --> PDF{path ends with .pdf?}

    PDF -->|yes| RP[read_pdf_bytes]
    RP --> TMP[Optional temp file for PyPDFLoader]
    TMP --> KIND_PDF[kind = pdf]

    PDF -->|no| RW[read_web_bytes]
    RW --> KIND_WEB[kind = web]

    KIND_PDF --> LS[load_and_split]
    KIND_WEB --> LS

    LS --> PPDF{kind pdf?}
    PPDF -->|yes| PY[PyPDFLoader]
    PPDF -->|no| WB[WebBaseLoader]

    PY --> SPLIT[RecursiveCharacterTextSplitter]
    WB --> SPLIT
    SPLIT --> TAG[tag_chunks: ingest_source_id]
```

**Detection rule:** URL path ends with `.pdf` → PDF. Otherwise → web (e.g. LangChain agents HTML).

---

## Chroma persist — create, append, replace

```mermaid
flowchart TD
    P[persist_chunks_to_chroma] --> OPEN[open_vector_store]
    OPEN --> EMPTY{Chroma empty?}

    EMPTY -->|yes| CREATE[Chroma.from_documents — first ingest]
    EMPTY -->|no| DEL{prior source exists<br/>or --force?}

    DEL -->|yes| DELETE[delete_source_chunks by ingest_source_id]
    DEL -->|no| ADD
    DELETE --> ADD[vector_store.add_documents]

    CREATE --> DONE([vectors on disk])
    ADD --> DONE
```

### What Chroma stores per chunk

| Field | Contents | Used for |
|-------|----------|----------|
| **Embedding** | Full float vector from Watsonx | Similarity search |
| **Document** | Full chunk text (`page_content`) | LLM context in chat |
| **Metadata** | `ingest_source_id`, `page`, PDF fields… | Source labels, delete-by-source |

**`--force` does not duplicate:** delete all rows for that `ingest_source_id`, then add fresh chunks.

---

## Manifest — the dedupe ledger

**Path:** `data/ingest_manifest.json`

```mermaid
flowchart LR
    INGEST[ingest_source] -->|writes| M[(manifest)]
    M -->|hash match| SKIP[Skip embed]
    M -->|hash changed| UPDATE[Delete old chunks + re-embed]
    CHAT[capstone_01_chat] -.->|does not read| M
    CHAT --> CHROMA[(Chroma only)]
```

Chat never opens the manifest. It only needs Chroma. The manifest is for **you** and ingest skip logic.

---

## Shared config (`capstone_shared.py`)

Both ingest and chat import the same embedding factory — **critical for search quality.**

| Constant | Value | Role |
|----------|-------|------|
| `CHROMA_DIR` | `data/chroma_01` | On-disk vector store |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | 500 / 50 | Splitter settings |
| `EMBED_PARAMS` | Watsonx, **no** `TRUNCATE_INPUT_TOKENS: 3` | Full-text embed at ingest |
| `METADATA_SOURCE_KEY` | `ingest_source_id` | Delete + filter by source |

**Trap (course vs capstone):** Labs use `TRUNCATE_INPUT_TOKENS: 3` for tiny demos. Capstone must embed **full** chunk text and full questions (via same params at query time). If you change `EMBED_PARAMS`, run `--corpus --force` to rebuild vectors.

---

## Function map (quick reference)

```
main()
├── --list      → cmd_list()
├── --corpus    → cmd_corpus() → ingest_source() × N
├── --web       → cmd_web()    → ingest_source() × N
└── positional  → ingest_source()

ingest_source()
├── read_source_bytes()
├── load_and_split()
│   ├── PyPDFLoader  OR  WebBaseLoader
│   ├── make_splitter()
│   └── tag_chunks()
└── persist_chunks_to_chroma()
    ├── make_embedding_model()  ← capstone_shared
    ├── delete_source_chunks()  (if update/force)
    └── add_documents() / from_documents()
```

---

## Run order (copy-paste)

```powershell
D:\py_venv\rag_application_builder_foundation\set_env.ps1
cd D:\Workarea\learning\playground\langchain\capstone

python capstone_01_ingest.py --corpus
python capstone_01_ingest.py "https://docs.langchain.com/oss/python/langchain/agents"
python capstone_01_ingest.py --list
```

After changing embed settings:

```powershell
python capstone_01_ingest.py --corpus --force
```

---

## Traps

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Chat has nothing to search | Ingest never run | `--corpus` then `--list` |
| Same wrong chunks for every question | Truncated embed params + old vectors | Fix `EMBED_PARAMS`, `--force` |
| Duplicate LangChain chunks | Same PDF ingested under two URLs/paths | One canonical `source_id`; delete stale rows |
| `--force` still feels “stale” | Only re-ingested one source | `--corpus --force` for all PDFs |
| Web ingest fails | Bad URL or network | Check URL in browser; `set_env.ps1` |

---

## Related

- Chat flow: [`capstone_01_chat_flow.md`](capstone_01_chat_flow.md)
- Debug retrieval (no LLM): [`debug_retrieval.py`](debug_retrieval.py)
- Corpus list: [`corpus_sources.json`](corpus_sources.json)