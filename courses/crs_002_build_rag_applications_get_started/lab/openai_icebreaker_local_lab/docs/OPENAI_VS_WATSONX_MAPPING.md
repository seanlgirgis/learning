# OpenAI vs watsonx Mapping

This lab copies the Coursera Icebreaker architecture and replaces IBM watsonx with OpenAI.

**Safe sentence:** We changed the provider, not the RAG architecture.

## Side-by-side

| Lab idea | IBM watsonx (Coursera) | Local OpenAI version |
|---|---|---|
| Embedding model | `WatsonxEmbeddings` | `OpenAIEmbedding` |
| LLM | `WatsonxLLM` | `OpenAI` (LlamaIndex adapter) |
| Auth / config | watsonx URL + project ID | `OPENAI_API_KEY` |
| Embedding model ID | Granite embedding model | `text-embedding-3-small` (configurable) |
| LLM model ID | `ibm/granite-4-h-small` | `gpt-4o-mini` (configurable) |
| Profile data (learning) | Mock JSON | `data/mock_linkedin_profile.json` |
| Chunking | `SentenceSplitter` | same |
| Index | `VectorStoreIndex` | same |
| Answers | `index.as_query_engine(...)` | same |
| UI | Gradio | Gradio |

## Function name aliases

In `modules/llm_interface.py`:

```text
create_watsonx_embedding  →  create_openai_embedding
create_watsonx_llm        →  create_openai_llm
```

Same names as the course notebook; different provider underneath.

## What stays identical

```text
profile dict → Document → nodes/chunks → embeddings → index → query engine → answer
```

The embedding model helps **find** relevant chunks. The LLM **writes** the final answer from those chunks.