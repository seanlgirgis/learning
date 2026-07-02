# RAG pipeline glossary

Short definitions for Module 3 study bubbles. Upgrade as we learn.

## Source

Raw knowledge **outside** LlamaIndex: files, folders, APIs, databases, web pages, cloud blobs. Not yet a `Document`.

## Loader

Code that **reads** a source and returns `list[Document]`. Example: `SimpleDirectoryReader(...).load_data()`.

## Document

LlamaIndex object with `.text` (body) and `.metadata` (dict of tags). One loaded file or logical unit.

## Metadata

Key–value tags on a `Document` or node — e.g. `file_name`, `file_path`, `source`. Helps tracing and filtering.

## Node

A **chunk** after splitting. LlamaIndex often uses `TextNode` under the hood. Smaller than a full Document.

## Chunk

A piece of text sized for retrieval (token/character limits). Same practical meaning as **node** in this course.

## Embedding

A list of numbers (vector) representing text meaning. Similar text → similar vectors. Used for search, not for reading by humans.

## Index

Data structure built from nodes + embeddings. Enables fast lookup. `VectorStoreIndex` embeds and stores in one step.

## Vector Store

Storage for embedding vectors keyed by node id. Often inside the index (in-memory in labs).

## Retriever

`index.as_retriever()` — embeds the question, returns top‑k matching **chunks**. No generated answer.

## Query Engine

`index.as_query_engine()` — retrieve + fill prompt template + call LLM. Returns a natural language **response**.

## LLM

Large language model (e.g. OpenAI `gpt-4o-mini`). Generates text from prompt + context. Course may say watsonx; local labs use OpenAI.

## Response

Also called **Answer** in the map — the final string shown to the user after `.query()`.