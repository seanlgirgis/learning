# 05 — Data Processing

**File:** `modules/data_processing.py`

## Three RAG steps in one module

```text
profile dict
    → JSON string
    → Document (loaded text object)
    → SentenceSplitter → nodes/chunks
    → OpenAI embeddings
    → VectorStoreIndex (searchable memory)
```

| Function | OpenAI? |
|---|---|
| `split_profile_data` | No — local chunking |
| `create_vector_database` | **Yes — embeddings** |
| `verify_embeddings` | No — checks index object |

## Why chunk?

Smaller pieces improve retrieval. One profile JSON may become one or more nodes depending on size and `CHUNK_SIZE`.

## Test (costs embedding tokens)

```bash
python tests/test_data_processing.py
```

Uses mock profile data. OpenAI is called when chunks are embedded.

Only run when you accept embedding cost.

## Next step

[06_query_engine.md](06_query_engine.md)