# Module 3 — file-by-file index

Work **in filename order**. One card = every section of that file.

| # | Source | Card | After reading |
|---|--------|------|---------------|
| 1 | `01.md` | [01.md.md](./01.md.md) | concepts: Document, Node, SimpleDirectoryReader, SentenceSplitter |
| 2 | `02.md` | [02.md.md](./02.md.md) | concepts: VectorStoreIndex, retriever, synthesizer, query engine |
| 3 | `03.png` | [03.png.md](./03.png.md) | skip (logo) |
| 4 | `04.md` | [04.md.md](./04.md.md) | open `05.pdf.md` |
| 5 | `05.pdf` | [05.pdf.md](./05.pdf.md) | icebreaker lab (mock data) |
| 6 | `06.jpg` | [06.jpg.md](./06.jpg.md) | retake quiz |
| 7 | `07.md` | [07.md.md](./07.md.md) | recap |
| 8 | `08.pdf` | [08.pdf.md](./08.pdf.md) | review before quiz |
| 9 | `09.md` | [09.md.md](./09.md.md) | whole-course recap |
| 10 | `10.md` | [10.md.md](./10.md.md) | optional links |

**LangChain (M1) vs LlamaIndex (M3):**

| Step | LangChain (your M1 scripts) | LlamaIndex (M3) |
|------|------------------------------|-----------------|
| Load | `TextLoader`, `PyPDFLoader` | `Document`, `SimpleDirectoryReader` |
| Split | `CharacterTextSplitter` | `SentenceSplitter` → **Nodes** |
| Index | `Chroma.from_documents` | `VectorStoreIndex` (embed + store **one step**) |
| Query | `RetrievalQA` chain | `as_query_engine()` or `as_retriever()` + synthesizer |

PDF extract: `../../_extracted/module3/`