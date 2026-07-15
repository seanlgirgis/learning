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
| 2026-07-11 | Foundations · gen vs disc | Predict loan default from history? | generative | **discriminative** | "AI task" felt generative; default = classify/predict outcome | needs_repetition |
| 2026-07-11 | Foundations · gen vs disc | Summarize PDF into 5 bullets? | generative | **Correct** | Create new text = generative | solid |
| 2026-07-11 | Foundations · FM vs LLM | GPT / Granite: foundation, LLM, or both? | LLM | **both** | Stopped at "language model"; missed that LLM ⊂ foundation models | needs_repetition |
| 2026-07-11 | Foundations · FM vs LLM | One pretrained model, many tasks via prompting? | LLM | **foundation model** | Defaulted to LLM; quiz word for multi-task base is foundation model | needs_repetition |
| 2026-07-11 | Foundations · FM vs LLM | Every LLM is FM; not every FM is only LLM? | True | **Correct** | Clarified after pushback; subset vs quiz contrast | solid |
| 2026-07-11 | Foundations · prompt eng | Changes weights or runtime instructions/context? | runtime | **Correct** | — | solid |
| 2026-07-11 | Foundations · shots | Three labeled tickets then label a fourth? | few-shot | **Correct** | 2+ examples = few-shot | solid |
| 2026-07-11 | Foundations · self-consistency | Reliability via A weights B multi-sample C vector DB? | B | **Correct** | multiple samples + agree | solid |
| 2026-07-11 | PromptTemplate | PromptTemplate.__________("Explain {topic}.") | from_template | **Correct** | — | solid |
| 2026-07-11 | ChatPromptTemplate | ChatPromptTemplate.__________([("human", "{q}")]) | invoke | **from_messages** | Confused constructor with fill/run step | needs_repetition |
| 2026-07-11 | Templates · mental model | from_template vs from_messages after labs 01–02 | blanks only vs blanks + turns | **Correct framing** | fill still dict for both | solid |
| 2026-07-11 | Templates · blanks location | Can blanks only be in human content, not system? | (hypothesis: not in system) | **Blanks OK in any role content** | blanks = inside content strings; any turn | needs_repetition |
| 2026-07-11 | Templates · roles | Types of turns: system / human / ai | confirmed | **Correct** (crs_001 core trio) | everyday: system/user/assistant | solid |
| 2026-07-11 | Tutor · 01b pipeline | prompt.invoke demo vs chain.invoke real path | code clear | **Correct** | fill-only line is teaching only | solid |
| 2026-07-11 | Invoke trio · billing | ChatOpenAI() alone charges? | no — charge on invokes | **Correct** | build object free; model/chain invoke costs | solid |
| 2026-07-11 | Tutor · 2b | from_messages for turns; chain.invoke = fill + call | confirmed after run | **Correct** | A demo only; B is real path | solid |
| 2026-07-12 | Few-shot | FewShotPromptTemplate is dedicated few-shot class | confirmed | **Correct** | examples + example_prompt + prefix/suffix | solid |
| 2026-07-12 | ChatPromptTemplate | Use from_messages for chat turns | confirmed | **Correct** | list of (role, content) | solid |
| 2026-07-12 | Templates · unified model | 3 classes build; template.invoke=prepare; chain.invoke=LLM | Sean summary | **Correct** | chat → .messages; string → .to_string() | solid |
| 2026-07-12 | LCEL · pipe | Which step hits network in prompt\|model\|parser? | model | **Correct** | prompt prepare; parser local | solid |
| 2026-07-12 | LCEL · name | prompt\|model is an LCEL chain? | T | **Correct** | LCEL = LangChain Expression Language; chain is the result | solid |
| 2026-07-12 | LCEL · StrOutputParser | Main job A call B string C retrieve? | B | **Correct** | reshape model output to str | solid |
| 2026-07-12 | LCEL · sequence vs parallel | prompt\|model\|parser is? | sequence | **Correct** | dependent steps use | | solid |
| 2026-07-12 | LCEL · parallel | title + tags independent from one article? | parallel | **Correct** | RunnableParallel fan-out | solid |
| 2026-07-12 | Structured output | Flask needs fields → free text or JSON? | B structured/JSON | **Correct** | apps need predictable fields | solid |
| 2026-07-12 | MessagesPlaceholder | Slot only; app owns history; N+vector M not built-in | no / your app | **Correct** | hybrid memory is app design | solid |
| 2026-07-12 | Chain vs memory vs agent | Italy population via tool use? | agent | **Correct** | agent = pick tools; was prior quiz trap | solid |
| 2026-07-12 | Chain vs memory vs agent | What did I ask two messages ago? | memory | **Correct** | continuity across turns | solid |
| 2026-07-12 | History loop | After one ask, how many appends? | 1 | **2** (Human + AI) | counted turns as 1 item not 2 messages | needs_repetition |
| 2026-07-12 | History loop | After 3 asks, len(history)? | 6 | **Correct** | 3×2 messages | solid |
| 2026-07-12 | Module 3 delivery | LCEL chain lives mainly where? | B model.py | **Correct** | Flask is door; model is brain | solid |
| 2026-07-12 | RAG · phases | Building index from PDFs? | build time | **Correct** | prepare knowledge before questions | solid |
| 2026-07-12 | RAG · embed | Embedding is? | B numeric meaning vector | **Correct** | not the file, not the route | solid |
| 2026-07-12 | Readiness gate | 4-Q pipe/charge/query/chunk | all solid | **Pass** | Q4 polish: context window + retrieval primary on quizzes | solid |

## Concepts to revisit

- **Generative vs discriminative** — label/outcome = disc; create new content = gen (tutor review 2026-07-11)
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