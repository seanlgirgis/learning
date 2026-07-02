# GROK Memory

Persistent conventions and decisions for `D:\Workarea\learning`.

## Full Context Export

The complete durable context export lives at:

```text
sean_girgis_memory_context_export_2026-06-15.md
```

Use that file for deep detail on career history, job search, DataCamp/Coursera progress, ALOK, LifeVault, RemNote, and related projects. **Confirm anything time-sensitive** (employment, interviews, course progress) rather than assuming it is still current.

---

## About Sean Girgis (Summary)

### Identity & Situation

- **Name:** Sean Girgis — `@seanlgirgis`, `seanlgirgis@gmail.com`
- **Location:** Richardson, Texas (Dallas–Fort Worth); prefers **remote** work
- **Background:** Senior Data Engineer, 20+ years enterprise experience (~8 years Citigroup); left Citi end of 2025
- **Current employment (as of export):** Joined **LTIMindtree** ~May 28–29, 2026; BOA client work via Frisco onboarding
- **Horizon:** Plans to work ~15 more years; near-term income need alongside longer-term technical growth

### Career Direction

**Primary targets:** Python, PySpark, SQL, ETL/ELT, AWS, data engineering, forecasting, RAG/AI applications, vector DBs, text processing — practical application building over deep ML research.

**Secondary strengths:** Observability/APM (Dynatrace, Splunk), capacity planning, performance engineering, FastAPI, Kubernetes/EKS, IaC, cost optimization.

### Learning Style (Critical — READ FIRST)

Sean has **ADD/ADHD**. Responses must stay **short — about one page max**, never textbook-length.

**Default response size:** ~1 A4 page or less. If more is needed, split across multiple turns.

Sean learns best through **very small, explicit, bite-sized steps**:

1. One small explanation
2. One tiny task or question
3. **Wait for Sean's response** before continuing

- No large lesson dumps, no walls of text, no exhaustive lists unless asked
- Make hidden assumptions explicit; revisit concepts from multiple angles when needed
- ADD/ADHD affects focus — brevity and pacing are non-negotiable
- **Theory-centered** documentation; explain code clearly, don't just list it
- Interactive pacing is preferred over monologue-style teaching

### Training mode (agent must follow)

Sean is being **trained**, not just answered. The agent should:

1. **Log questions** — Append `docs/TRAINING_LOG.md` (topic, answer, trap, status).
2. **Keep tally** — Update `docs/COURSE_OPERATIONS.md` (scores, deck count, backlog, enforcement checks).
3. **Enhance without asking** — Sean authorized: fix stale docs, add RemNote decks, add bubble maps when gaps appear.
4. **Track weak spots** — Revisit logged traps; add targeted `source_cards/05_xx` decks.
5. **Wait** — One teaching beat, then pause for Sean's response.

Active course ops: `courses/crs_001_develop_generative_ai_applications_get_started/docs/COURSE_OPERATIONS.md`

### Development Preferences

- Reusable mechanics → **shared library** (`D:\py_libs\rag_foundation`), not copy-paste across labs
- Production-quality library code: typed, documented, tested, reusable
- Generalize first → test → example → replace duplicated local code
- Preserve **exact canonical filenames**; no `_updated`, `_final`, `_new` suffixes
- Relative links inside repos; consolidated digests and reference guides
- Codex-ready prompts: exact paths, files, validation commands, scope limits
- Sean runs commands manually

### Current Learning Priorities (Practical Order)

1. Developing AI application skills
2. Coursera IBM RAG specialization (`crs_rag_for_generative_ai_applications`)
3. DataCamp materials consolidated and certification-ready
4. RAG Application Builder Foundation
5. Expand `rag_foundation` shared library
6. Observability, token/cost/budget tracking in AI systems
7. Production-style RAG and agent applications

### Related Project Roots (Established Elsewhere)

| Area | Path |
|------|------|
| Unified online learning (DataCamp + Coursera) | `D:\Workarea\StudyBook\study_maps\DataCamp` |
| RAG Application Builder Foundation | `...\skill_tracks\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation` |
| Shared Python library | `D:\py_libs\rag_foundation` |
| Foundation venv | `D:\py_venv\rag_application_builder_foundation` |
| Private BOA/LTIM second brain | `D:\Workarea\ALOK` |
| This learning workspace | `D:\Workarea\learning` |

**Naming:** Coursera folders use `crs_` prefix; DataCamp generally has no prefix. Do not move established roots without explicit agreement.

### Standing Constraints

- Teach in small bites; don't assume hidden steps were understood
- No secrets, banking-confidential info, or unnecessary PII in Git
- OpenAI primary provider; IBM watsonx planned later
- Include monitoring and budget visibility in AI application architecture
- RemNote for spaced repetition (multiple-choice primary mode)

---

## Session Files (GROK_ prefix)

Always use the `GROK_` prefix for agent/memory files in this folder:

| File | Purpose |
|------|---------|
| `GROK_MEMORY.md` | Long-lived conventions, decisions, and lessons learned |
| `GROK_AGENTS.md` | Agent roles, workflows, and handoff rules |
| `GROK_RUNBOOK.md` | Environment setup, commands, and operational procedures |
| `GROK_CURRENT_STATE.md` | Active work, recent changes, and next steps |

## Project Purpose (This Repo)

Learning path for courses, study materials, and labs covering:

- Python
- RAG (Retrieval-Augmented Generation)
- AI applications
- DataCamp, Coursera, and similar platforms

Complements (does not replace) the established StudyBook/DataCamp roots above.

## StudyBubble Maps (Canonical Style)

**Recall doc:** `Study_bubbles/MODEL_MAPS.md` — say "remember our model maps" to use this.

| Type | Path |
|------|------|
| Landscape | `Study_bubbles/references/model_maps/landscape/iac_why_terraform_exists.html` |
| Workflow | `Study_bubbles/references/model_maps/workflow/terraform_core_workflow.html` |

All builds auto-apply style `terraform_learnterraform_v1`. Max **20** bubbles; sweet spot 8–15. CLI: `python tools/studybubble.py model-maps`

**Layout (engine default):** drag auto-saves in browser; `import-layout` bakes into HTML. See `Study_bubbles/docs/LAYOUT_PERSISTENCE.md`

## Coursera specialization (canonical URL)

**RAG for Generative AI Applications** — four IBM courses (`crs_001`–`crs_004`):

https://www.coursera.org/specializations/rag-for-generative-ai-applications

**Course 1 (`crs_001`):** Develop Generative AI Applications: Get Started

https://www.coursera.org/learn/develop-generative-ai-applications-get-started?specialization=rag-for-generative-ai-applications

Catalog: `catalog/courses.yaml`, `catalog/paths.yaml` · Path hub: `paths/coursera_ibm_gen_ai_engineering/index.html`

## Navigation (HTML)

- **Relative paths only** in HTML links and breadcrumbs — no `file:///` URLs, no `D:\...` paths unless unavoidable (e.g. venv outside repo).
- Cross-repo links to StudyBook use sibling relative paths from repo root, e.g. `../StudyBook/study_maps/DataCamp/...`.
- Course packages link up via `../../index.html` (Learning Hub), `../index.html` (Courses), and path index as needed.

## Repository Model (Implemented)

- **Hub:** `index.html` at repo root — linked HTML navigation.
- **Courses** = `courses/<id>/` — Coursera `crs_`, DataCamp no prefix.
- **Units** = `units/<id>/` — skills (`skill_`), interview (`interview_`), other topic packs.
- **Paths** = `paths/<id>/` — ordered views over courses + units via `catalog/paths.yaml`.
- **Templates** = `shared/templates/` (StudyBook Course_starter + path/unit templates).
- **Catalog** = `catalog/courses.yaml`, `units.yaml`, `paths.yaml`.
- Planning docs in `planning/` (not `GROK_` prefixed).

## Structure Principles

- Keep a clean, navigable layout with **numbered labs** when appropriate (e.g. `lab_01/`, `lab_02/`).
- Focus on **small, bite-sized, reusable** work — one concept or exercise per unit.
- Prefer self-contained lab folders with a short README when context is needed.
- Extract reusable utilities into `rag_foundation` or shared modules when patterns repeat.

## Environment

- **Python venv activation (required before any Python command):**
  ```powershell
  D:\py_venv\rag_application_builder_foundation\set_env.ps1
  ```
- Python 3.13.11 in foundation venv; navigates to foundation lab via `RagCode` helper in `set_env.ps1`.

## Naming & Organization

- Descriptive, lowercase folder names with underscores (e.g. `rag_basics`, `lab_01_intro`).
- Course folders: `datacamp/`, `coursera/`, `rag/`, `python/`.
- Numbered imports/files: `01_...`, `02_...` when sequence matters.

## Notes

- Update `GROK_CURRENT_STATE.md` at the end of each session.
- Record non-obvious decisions here; defer to the full export for historical detail.