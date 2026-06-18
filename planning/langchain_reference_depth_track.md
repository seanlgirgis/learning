# LangChain Depth Track — Reference + crs_001

**Decision (locked 2026-06-17):** **Reference first, crs_001 second.** Same item-by-item rhythm in each phase. More iterations = more remembering. Do not sync course materials until the reference page for that topic is deep.

**Workflow:** One item per session → you review → discuss → update this file.

**Paths:**

| Layer | Root | Role |
|-------|------|------|
| Playground | `playground/langchain/` | Runnable labs — source of traps & examples |
| Reference | `reference/langchain/` | Deep lookup — **Phase A** (active) |
| Course | `courses/crs_001_develop_generative_ai_applications_get_started/` | Coursera package — **Phase B** (after A gate) |

---

## Phases (order is fixed)

| Phase | What | Gate to start |
|-------|------|----------------|
| **A — Reference deepen** | Modules 01–11 + 16 recipes | — (active) |
| **A′ — Reference delta** | Modules 12–19, labs 23–35, guides | ✅ Modules 12–19 done (2026-06-18) |
| **B — crs_001 sync** | Field guides, source_cards, bubbles, course links | A complete for that topic (module deep + recipe if any) |
| **C — Re-education** | Live recall / rebuild / compare / trap drills with Grok | B done for that topic (or A for early spine 01–03) |

**Why reference first:** One gold template per topic; crs_001 gets a copy-paste-sync pass, not a second draft. Avoids rewriting field guides twice.

---

## 11-point depth checklist (reference pages)

1. Job (help-desk story)
2. Problem without it
3. Object lifecycle
4. Flow diagram
5. Properties + “if wrong then…”
6. Minimal + full lab example
7. Confusion matrix
8. Coursera → 1.x import bridge
9. Trap box (≥3 real errors)
10. Recall drills (≥3)
11. Links (lab, recipe, bubble)

**Score:** items present / 11.

---

## Phase A — Reference module queue

| ID | Page | Score | Status | crs_001 sync (Phase B) |
|----|------|-------|--------|-------------------------|
| 01 | `modules/01-prompt-template.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 02 | `modules/02-watsonx-llm.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 03 | `modules/03-lcel-pipe.html` | 11/11 | ✅ Gold standard | Pending |
| 04 | `modules/04-output-parser.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 05 | `modules/05-runnable-lambda.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 06 | `modules/06-model-inference.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 07 | `modules/07-watson-helpers.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 08 | `modules/08-chat-messages.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 09 | `modules/09-gen-params.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 10 | `modules/10-chat-prompt-template.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 11 | `modules/11-json-output-parser.html` | 11/11 | ✅ Deep pass 1 | Pending |
| 12 | `modules/12-document-loaders.html` | 11/11 | ✅ A′ delta | Labs 23–25 |
| 13 | `modules/13-text-splitters.html` | 11/11 | ✅ A′ delta | Labs 26–27 |
| 14 | `modules/14-embeddings.html` | 11/11 | ✅ A′ delta | Lab 28 |
| 15 | `modules/15-chroma-vectorstore.html` | 11/11 | ✅ A′ delta | Lab 29 |
| 16 | `modules/16-retrievers-rag.html` | 11/11 | ✅ A′ delta | Labs 30–32 |
| 17 | `modules/17-memory.html` | 11/11 | ✅ A′ delta | Lab 33 |
| 18 | `modules/18-classic-chains.html` | 11/11 | ✅ A′ delta | Lab 34 |
| 19 | `modules/19-agents-tools.html` | 11/11 | ✅ A′ delta | Lab 35 |

**A gate (for A′ delta):** all 11 rows ≥ 8/11 average — **✅ met**. **A′ modules 12–19:** **✅ complete**.

## Phase A′ — Module queue (complete)

| ID | Page | Labs |
|----|------|------|
| 12–19 | see table above | 23–35 |

**NEXT:** Capstone practice → [langchain_capstone_projects.md](langchain_capstone_projects.md) · Phase B per-module field guides

---

## Phase A — Recipe queue

| Page | Score | Status |
|------|-------|--------|
| `recipes/summarize.html` | 11/11 | ✅ Gold standard |
| Other 15 recipes | 11/11 | ✅ Depth pass 1 (2026-06-18) |

---

## Phase A′ — Delta ✅

Modules 12–19 shipped 2026-06-18. Optional guides still queued: `lc1x-migration`, `rag-pipeline`, `react-internals`.

---

## Phase B — crs_001 sync queue (starts after A row is deep)

Per reference module, touch these **in order** (item-by-item, same chat rhythm):

| Step | crs_001 target | Action |
|------|----------------|--------|
| B1 | `study_pages/langchain_code_patterns.html` | Add / align section → link to reference module |
| B2 | `study_pages/concept_and_code_quick_lookup.html` | Trap + confusion one-liners from reference |
| B3 | Matching `source_cards/05_*.md` | Cards mirror recall drills + traps |
| B4 | `bubbles/` node if exists | ID lockstep with module section |
| B5 | `index.html` + field guides | Relative link to `reference/langchain/modules/…` |
| B6 | `docs/TRAINING_LOG.md` | Log any new study questions from sync |

**B batch order (after A gate on 01–11):** sync 01 → 02 → 03 → … → 11 (then recipes), then A′ topics when they exist.

| Ref module | B status | Notes |
|------------|----------|-------|
| Spine sync | 🟡 Started | `langchain_code_patterns.html`, `concept_and_code_quick_lookup.html`, course `index.html`, source_cards 05_06 |
| 01–19 field guides | 🔒 | Per-chapter sync next — item-by-item |

---

## Phase C — Re-education (after B per topic)

| Session type | Uses |
|--------------|------|
| Recall | Confusion matrix + trap boxes only |
| Rebuild | Skeleton lab in `playground/` — reference closed |
| Compare | Two modules side by side — prose answer |
| Trap drill | Random trap → you name fix |

Log questions to `courses/crs_001/.../docs/TRAINING_LOG.md`.

**Quiz rule (Sean):** Two files only — A) `watson_helper` + `generate()` B) `watson_llm` + invoke/pipes/embeddings. Aliases removed (2026-06-17). Bubble: `bubbles/outputs/crs_001_watson_two_routes.html`.

**C for spine 01–03:** can start after Sean reviews deep pass 1 (does not require full B).

---

## Session log

| Date | Phase | Item | Outcome |
|------|-------|------|---------|
| 2026-06-17 | A | Plan + audit | Checklist; hub audit table |
| 2026-06-17 | A | 01, 02, 03, summarize | Deep pass 1; CSS patterns |
| 2026-06-17 | — | Strategy locked | Reference first → crs_001 sync → re-education |
| 2026-06-17 | A | 04 StrOutputParser | Deep pass 1 complete |
| 2026-06-17 | A | 05 RunnableLambda | Deep pass 1 complete |
| 2026-06-17 | A | 06 ModelInference | Deep pass 1 complete |
| 2026-06-17 | A | 07 Watson helpers | Deep pass 1 complete |
| 2026-06-18 | A | 08 Chat messages | Deep pass 1; string vs message-list spine |
| 2026-06-18 | A | 09 GenParams | Deep pass 1; build-time params spine |
| 2026-06-18 | A | 10 ChatPromptTemplate | Deep pass 1; two-pattern spine |
| 2026-06-18 | A | 11 JsonOutputParser | Deep pass 1; Pydantic vs hand-written spine |
| 2026-06-18 | A′ | Modules 12–19 | Full playground 23–35 coverage |
| 2026-06-18 | Recipes | 15 recipes | 7-section depth pass (summarize gold) |
| 2026-06-18 | Guides | RAG + ReAct | `reference/langchain/guides/` |
| 2026-06-18 | B (partial) | crs_001 spine | code patterns, quick lookup, index, source_cards |
| — | — | **Capstones · B per-module** | **NEXT** |

---

## Per-session rhythm

1. State **phase + NEXT item** from tables above.
2. Deepen or sync **one** file.
3. You skim; we discuss one round.
4. Update this file + `GROK_CURRENT_STATE.md`.

---

## Open

- [ ] Sean review: 03 LCEL pipe gold standard
- [ ] Go **04** (Phase A)?
- [ ] Optional early **B pilot** on 01–03 only after 04–11 done? (default: **no** — full A then B)