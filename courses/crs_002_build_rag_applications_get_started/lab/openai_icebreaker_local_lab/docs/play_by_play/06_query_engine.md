# 06 — Query Engine

**File:** `modules/query_engine.py`  
**Mental model:** retriever + prompt + LLM (not a direct `llm.invoke`)

## What `query_engine.query()` does

```text
question
    → embed question
    → retriever finds top-k chunks from index
    → prompt template fills {context_str}
    → LLM writes answer
```

This is **not** sending the question straight to the LLM without profile context.

## Two entry points

| Function | Purpose |
|---|---|
| `generate_initial_facts` | Three icebreaker facts |
| `answer_user_query` | Chat follow-ups |

Both use `index.as_query_engine(...)` with different prompt templates from `config.py`.

## OpenAI usage

**Yes** — embeddings for retrieval + LLM for the answer.

## Test (most expensive test script)

```bash
python tests/test_query_engine.py
```

Runs full pipeline including initial facts and one chat question.

Run only when you explicitly want to spend embedding + LLM tokens.

## Next step

[07_cli_main.md](07_cli_main.md)