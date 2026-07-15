# CRS 003 · Module 1 — Source map

Canonical source: `source_material/module1/`  
Official module name: **Introduction to Vector Databases and Chroma DB**

## Lessons (Coursera outline)

| Lesson | Focus |
|--------|--------|
| 0 | Welcome / course frame |
| 1 | Vector databases + similarity search |
| 2 | Exploring Chroma DB |

## File index (learning path order)

| Order | File | Teach as |
|------:|------|----------|
| 1 | `003.md`, `004.md` | Course welcome, M1/M2 outline, objectives |
| 2 | `002.ibmwatsonx.data` | Optional IBM platform note (not core theory) |
| 3 | `007.md` | Vectors, vector DB importance, book example |
| 4 | `008.pdf` | Vector DB vs traditional; library vs full CRUD DB |
| 5 | `009.md` | Types of vector DBs; dedicated vs “supports vector search” |
| 6 | `010.md` | Use cases (media, recs, geo, social) |
| 7 | `014.optional.md` / podcast | Same as L1 concepts, conversational |
| 8 | `012.lab.md` + `013…ipynb` | Manual metrics: L2, dot product, cosine |
| 9 | `017.md` | Chroma architecture, collections, workflow, HNSW intro |
| 10 | `018.pdf` | Chroma filtering (`where`, `where_document`) |
| 11 | `019.pdf` | HNSW params + Chroma query (pandas animal vs library) |
| 12 | `020Lab.md` + `021.lab.pdf` | Text similarity lab with Chroma + SentenceTransformer |
| 13 | `022.lab.md` | Lab recap podcast |
| 14 | `024.summary.md` | Module “you know” checklist |
| 15 | `025.pdf` | Cheat sheet (metrics + compare + Chroma tips) |
| — | `001.objectived.,md` | **Misaligned** — content matches Module 2 themes; do not use as M1 objectives |
| — | `005.md` | Whole certificate overview (context only) |
| — | `011.md` | Large PDF; secondary deep reading |
| — | images / mp3 | Visuals & audio support |

## Local labs (repo)

| File | Aligns to |
|------|-----------|
| `lab/python/001_similarity_search_by_hand.py` | Manual similarity (012/013) |
| `lab/python/002_chroma_similarity_search.py` | Chroma text search (020/021) |
| `lab/python/003_chroma_native_embedding_search.py` | Chroma embedding path |
| `lab/python/004_chroma_cosine_distance_search.py` | Distance / cosine space |

## Package build targets (M1)

- [ ] `study_pages/module1_field_guide.html` (spine)
- [ ] `source_cards/` (metrics, compare, Chroma, HNSW)
- [ ] `bubbles/` (pipeline + metric chooser)
- [ ] Tutor runbooks / commented labs as needed
- [ ] `docs/COURSE_OPERATIONS.md` + `TRAINING_LOG.md` when training starts
