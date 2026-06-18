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
| **Chroma dir** | Filing cabinet of **index cards** — each card has a vector “fingerprint” so similar questions pull the right cards |
| **Manifest** | **Checkout log** at the desk — “LangChain paper filed on Tuesday, hash abc123, 57 cards” |

Same PDF twice? Manifest says **skip**. New question? Chroma says **which chunks**.

---

## Paths (both scripts must agree on Chroma path)

```text
capstone/data/chroma_01/           ← CHROMA_DIR
capstone/data/ingest_manifest.json ← MANIFEST_PATH
```

---

## Flow

```text
INGEST (once per new/changed PDF)
  PDF → chunks → embed → write vectors → chroma_01/
                      → write source + hash → ingest_manifest.json

CHAT (many times)
  question → embed question → search chroma_01/ → top chunks → LLM answer
  (manifest not used)
```

---

## One sentence each

- **Chroma dir:** stores **searchable vectors** for RAG retrieval.
- **Manifest:** stores **ingest history** so unchanged PDFs are not re-embedded.

---

*Recall drill: cover the table, say out loud what each stores and which script reads it.*