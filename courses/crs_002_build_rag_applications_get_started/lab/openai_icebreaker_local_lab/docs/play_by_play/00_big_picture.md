# 00 — Big Picture

## What this lab is

A local copy of the Coursera **Icebreaker Bot** pattern:

- LlamaIndex for RAG
- Profile data as the knowledge source
- Query engine for grounded answers

**Difference:** Coursera used IBM watsonx. This folder uses **OpenAI**. The pipeline shape is the same.

## End-to-end flow

```text
Profile source
    → extraction (dict)
    → Document (loaded text)
    → nodes/chunks (smaller pieces)
    → embeddings (semantic fingerprints)
    → index (searchable memory)
    → query engine (retrieve + prompt)
    → LLM (final answer)
```

## Two roles of AI models

| Model | Job | Mental model |
|---|---|---|
| Embedding model | Find similar chunks | Search |
| LLM | Write the answer | Generation |

Safe sentence: The embedding model helps find relevant profile chunks; the LLM writes the final answer from those chunks.

## Mock mode (default for learning)

`mock=True` reads `data/mock_linkedin_profile.json`.

- No LinkedIn
- No Proxycurl
- No OpenAI in the extraction step

OpenAI is used later for embeddings and answers.

## Next step

[01_environment_setup.md](01_environment_setup.md)