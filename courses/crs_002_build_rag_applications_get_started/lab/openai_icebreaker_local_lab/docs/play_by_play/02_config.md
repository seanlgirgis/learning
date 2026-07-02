# 02 — config.py

## Goal

Understand settings and prompts **without** calling OpenAI.

## What lives here

| Setting | Purpose |
|---|---|
| `OPENAI_LLM_MODEL` | LLM for answers |
| `OPENAI_EMBEDDING_MODEL` | Model for chunk vectors |
| `CHUNK_SIZE` | How big each node/chunk is |
| `SIMILARITY_TOP_K` | How many chunks go into the prompt |
| `MOCK_DATA_PATH` | Local JSON for `mock=True` |
| `INITIAL_FACTS_TEMPLATE` | Prompt for icebreaker facts |
| `USER_QUESTION_TEMPLATE` | Prompt for chat Q&A |

Prompt placeholders:

- `{context_str}` — retrieved chunks
- `{query_str}` — user question

## Provider note

Coursera read watsonx IDs from the cloud IDE. This file reads OpenAI names from env or `.env`.

## Test (no OpenAI cost)

```bash
python tests/test_config.py
```

## Next step

[03_data_extraction.md](03_data_extraction.md)