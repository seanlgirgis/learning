# 04 — OpenAI Model Interface

**File:** `modules/llm_interface.py`  
**Mental model:** provider replacement layer

## Coursera vs local

| Coursera | Local |
|---|---|
| `create_watsonx_embedding()` | `create_openai_embedding()` |
| `create_watsonx_llm()` | `create_openai_llm()` |

Alias names `create_watsonx_*` still exist so you can map course notebooks.

## Two clients

```text
create_openai_embedding()  →  semantic search (vectors)
create_openai_llm()        →  answer generation (text)
```

Safe sentence: **Embeddings find; the LLM writes.**

Creating a client does not always mean an API call yet — embeddings run during indexing; the LLM runs during `query_engine.query()`.

## Test (no OpenAI cost)

```bash
python tests/test_llm_interface_imports.py
```

Only checks that functions import — does not call them.

## Next step

[05_data_processing.md](05_data_processing.md)