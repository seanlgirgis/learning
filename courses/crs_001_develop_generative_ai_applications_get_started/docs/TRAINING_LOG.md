# Training Log — CRS 001

Sean study questions and recall tracking. Agent appends rows during training sessions.

**Tally and backlog:** `COURSE_OPERATIONS.md` (same folder)

| Date | Topic | Question / source | Sean's answer | Correct | Confusion pattern | Status |
|------|-------|-------------------|---------------|---------|-------------------|--------|
| 2026-06-15 | LangChain · ChatPromptTemplate | RemNote `05` — which property holds the generated message list after `invoke`? | Leaning `messages.output` (screenshot) | `messages.messages` | Mixing invoke return shape with chain/parser `.output` | needs_repetition |
| 2026-06-15 | LangChain · ChatPromptTemplate | RemNote `05` cloze — `ChatPromptTemplate.__________((...))` | (asked via image) | `from_messages` | — | new |
| 2026-06-15 | LangChain · ChatPromptTemplate | RemNote `05` — which tuple is the current user request? | (asked via image) | `("human", "{question}")` | — | new |
| 2026-06-15 | LangChain · roles | Sean: trained on system/user/assistant; first time seeing `human` | Prior mental model = user | LangChain says `human` | API vs template vocabulary | needs_repetition |
| 2026-06-15 | LangChain · PromptTemplate | RemNote `05` cloze — `PromptTemplate.__________("Explain {topic}.")` | drill: `FromTemplate` → concept OK | `from_template` | Spelling: snake_case | improving |
| 2026-06-15 | LangChain · ChatPromptTemplate | drill — `ChatPromptTemplate.__________([("human", "{q}")])` | `from_template` then **`from_messages`** ✓ | `from_messages` | Brackets = list = from_messages | solid |
| 2026-06-15 | Coursera crs_001 quiz | Module quiz (5 Q) — in-context learning, zero-shot, LCEL pipe, PromptTemplate | **100%** (screenshot) | all correct | RemNote drills translating to platform | solid |
| 2026-06-15 | Coursera crs_001 quiz | Module quiz (7 Q) — prompt elements, format(), LCEL coercion, in-context, pipe | **100%** (screenshot) | all correct | Platform uses `format()` vocabulary; labs use `invoke()` | solid |
| 2026-06-16 | Coursera crs_001 quiz | LangChain components (5 Q) — sequential chain, memory, agents, parsers, chat models | **40%** (2/5) | Q1,Q4 only | Mapped sequential chain → memory/context; agent → memory; dynamic chat → prompt templates | needs_repetition |
| 2026-06-16 | LangChain · sequential chain | Q1 — primary function of sequential chain? | (passed quiz) | Pass output of one step as input to next | Concept was fuzzy pre-quiz; answered correctly under pressure | improving |
| 2026-06-16 | LangChain · memory | Q2 — continuity across interactions? | Sequential chains link outputs/inputs | **Memory** reads/writes historical data | Confused pipeline wiring with conversation history | needs_repetition |
| 2026-06-16 | LangChain · agents | Q3 — Italy population via agent? | Store query in memory | **LLM picks options + queries database** | Agent = reason + use tools, not just remember | needs_repetition |
| 2026-06-16 | LangChain · chat models | Q5 — workout bot, direct responses, no predefined instructions? | Prompt templates | **Chat models** | Prompt templates *are* predefined structure | needs_repetition |
| 2026-06-18 | Reference book | Modules 01–19 + recipes + guides shipped | — | — | Full playground 08–35 map live | new_material |
| 2026-06-18 | Phase B spine | crs_001 code patterns + quick lookup synced to reference | — | — | Watson routes, RAG, agents cards added | new_material |
| 2026-06-19 | Coursera crs_001 quiz | M2 — LCEL build order (template → PromptTemplate → pipe → invoke) | Picked create PromptTemplate first | **Define template with variables first** | Reordered steps; pipe before variables | needs_repetition |
| 2026-06-19 | Coursera crs_001 quiz | M2 — why text split long documents? | Reduce token count / API cost | **Chunks fit context windows** (+ retrieval) | Cost is side benefit, not primary reason | needs_repetition |
| 2026-06-19 | Coursera crs_001 quiz | M2 — LangChain memory | Read/write memory for continuity | **Correct** | — | solid |
| 2026-06-19 | Coursera crs_001 quiz | M2 — LCEL connect syntax | `prompt \| llm \| output_parser` | **Correct** | — | solid |
| 2026-06-19 | Playground capstone 04 | ReAct agent REPL — calculator vs `search_course_docs` routing | Live REPL: math + RAG + quit | **Correct** | Router mental model clicking; provider/agent LLM traps resolved earlier | solid |
| 2026-06-19 | Study materials | Light touch — `11-module2-quiz.md` added | — | 14 cards | Reinforce M2 quiz traps before M3 | new_material |
| 2026-06-19 | Coursera crs_001 | **Course complete — certificate earned** | M3 lab + final quizzes | — | Module 3 curl-proved; GUI preview N/A on SN | solid |
| 2026-06-19 | Documentation | Course finalize pass — study_pages, source_cards, bubbles, CODE_CATALOG | — | — | decks `12`/`13`; module3 + capstone bubble maps | new_material |

## Concepts to revisit

- **LCEL order** — define template with `{vars}` → `PromptTemplate` → `prompt | llm | parser` → `invoke` (Lab `08.lcel.1.py`)
- **Text split** — main reason: chunks fit **context window** + better retrieval; cost savings is secondary
- **Memory vs sequential chain vs agent** — memory = cross-turn history; sequential chain = fixed step wiring; agent = LLM picks tools (RemNote `11`, quiz 2026-06-16)
- **`chat_prompt.invoke()` return** → use `.messages` for the message list (lab `03_chat_prompt_template.py`)
- **Invoke trio** — `prompt.invoke` = prepare · `model.invoke` = generate · `chain.invoke` = run all (RemNote `09`)
- **Role naming** — Sean trained on `system / user / assistant`; LangChain templates use `system / human / ai` (same idea, different words)

## Next micro-drill (when ready)

1. **LCEL order:** list the four steps in order (no peeking).
2. **Text split:** one sentence — why shred a 50-page PDF?
3. **Memory vs chain vs agent:** one line each (RemNote `11`).
4. **String template:** `PromptTemplate.__________("Explain {topic}.")` → ?
5. **Chat template:** `ChatPromptTemplate.__________([("human", "{q}")])` → ?

## Module 3 backlog (Sean gleans Coursera — build after M3 done)

- Finish `chapter_03` field guide + Flask lab notes
- Source cards `06_*` (model selection, Flask, ops)
- Optional bubble: app lifecycle / Flask route flow
- Refresh `certification_review_digest.html` once exam-ready