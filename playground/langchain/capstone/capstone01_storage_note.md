# Capstone 01 — What stores what (Chroma dir vs manifest)

← [capstone01.md](capstone01.md)

Two files/folders under `capstone/data/`. Different jobs.

---

## At a glance

| | **Chroma dir** (`chroma_01/`) | **Manifest** (`ingest_manifest.json`) |
|---|-------------------------------|----------------------------------------|
| **What** | Vector database (folder) | Small JSON ledger (one file) |
| **Stores** | Chunk **text embeddings** + chunk metadata | **Which sources** were ingested + **content hash** |
| **Size** | Grows with every chunk | Tiny (one row per PDF) |
| **Used when** | **Retrieval** — “which chunks match this question?” | **Ingest** — “did we already embed this exact file?” |
| **Read by** | `capstone_01_chat.py` (and ingest when appending) | `capstone_01_ingest.py` only |
| **If missing** | Chat has nothing to search | Ingest can’t dedupe (would re-embed everything) |

---

## Layman

| Piece | Analogy |
|-------|---------|
| **Chroma dir** | Filing cabinet of **index cards** |
| **Manifest** | **Checkout log** at the desk |

---

## One sentence each

- **Chroma dir:** stores **searchable vectors** for RAG retrieval.
- **Manifest:** stores **ingest history** so unchanged PDFs are not re-embedded.

← KB: `D:\Workarea\KB\01_concepts\rag-vector-store-and-ingest-manifest.md`