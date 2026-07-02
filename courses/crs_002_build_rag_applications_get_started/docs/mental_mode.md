Yes — for your bubble diagram, use **main levels**, not code classes first.

Put the **center bubble** as:

```text
LlamaIndex RAG App
```

Then draw these main bubbles around it:

```text
1. Source
   Files, PDFs, folders, text.

2. Loader
   Reads source material into Document objects.

3. Documents
   Loaded text + metadata.

4. Nodes / Chunks
   Smaller pieces of the documents.

5. Embeddings
   Numeric meaning representation of each chunk.

6. Index / Vector Store
   Searchable memory built from chunks + embeddings.

7. Retriever
   Finds the best matching chunks for a question.

8. Query Engine
   Coordinates retrieval + LLM call.

9. GenAI Model
   Writes the final answer.

10. UI / App
   Gradio or chat screen the user interacts with.
```

The arrow flow is:

```text
Source → Loader → Documents → Chunks → Embeddings → Index → Retriever → Query Engine → LLM → Answer
```


Good. Now let’s turn the bubbles into **two groups**.

## Group 1 — Build time

This is when you prepare the documents.

```text
Source files
   ↓
Loader
   ↓
Documents
   ↓
Chunks / Nodes
   ↓
Embeddings
   ↓
Index / Vector Store
```

Meaning:

```text
“Prepare my knowledge so it can be searched.”
```

This usually happens **before the user asks a question**.

Example code shape:

```python
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
```


Yes. The **Loader bubble** means:

```text
“Where does the raw knowledge come from?”
```

Main loader sources:

```text
1. Single file
   One PDF, CSV, TXT, MD, DOCX.

2. Directory
   A folder with many files.

3. Recursive directory
   Folder + subfolders.

4. Filtered directory
   Only .md, only .pdf, exclude archive, etc.

5. Web page
   Load text from a URL.

6. Database
   Load rows from SQL or another database.

7. API
   Load text/data returned from a service.

8. In-memory text
   You create Document(text="...") yourself.

9. Cloud storage
   S3, Google Drive, SharePoint, etc., depending on connector/reader.
```

For your course, focus first on:

```text
File → Directory → Recursive/filter directory → Manual Document
```


