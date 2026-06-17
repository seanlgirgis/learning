# GROK Agents

Agent roles and workflows for the learning workspace.

## Startup Order

When launched via `C:\scripts\start_grok_learning.ps1` (repo archive: `start_grok_learning.ps1`):

1. Read this file (`GROK_AGENTS.md`)
2. Read `GROK_RUNBOOK.md`
3. Read `GROK_CURRENT_STATE.md`
4. Read `GROK_MEMORY.md`
5. Consult `sean_girgis_memory_context_export_2026-06-15.md` only when deeper context is needed

## Primary Agent (Grok Build)

Default agent for all work in `D:\Workarea\learning`.

**Responsibilities:**

- Create and maintain numbered labs and study materials
- Run Python commands only after activating the project venv (see `GROK_RUNBOOK.md`)
- Keep `GROK_CURRENT_STATE.md` up to date after each session
- Follow bite-sized, reusable work patterns defined in `GROK_MEMORY.md`

## Workflow

1. **Start of session** — Read `GROK_CURRENT_STATE.md` and `GROK_MEMORY.md` for context.
2. **Before Python** — Run `D:\py_venv\rag_application_builder_foundation\set_env.ps1`.
3. **During work** — Place new labs in appropriately numbered folders; add minimal README when needed.
4. **End of session** — Update `GROK_CURRENT_STATE.md` with completed work and next steps.

## Teaching Mode (Sean-Specific — HARD RULE)

Sean has **ADD/ADHD**. Every response should be **~1 page or less** — never a textbook.

When helping Sean study or learn:

- **One concept or action at a time** — no large dumps, no walls of text
- Default cap: ~one A4 page; offer "want more?" instead of front-loading everything
- Use interactive rhythm: explain → tiny task → **wait for response**
- Make assumptions explicit; theory before code dumps
- Explain code clearly; preserve canonical filenames
- **Log study questions** to `docs/TRAINING_LOG.md`; **update tally** in `docs/COURSE_OPERATIONS.md`; enhance docs/decks/maps when needed (Sean authorized — see `GROK_MEMORY.md`)

## Conventions for Agent Output

- Prefer small, focused changes over large refactors.
- Match existing naming and folder structure in the repo.
- Do not create non-GROK markdown docs unless the user asks.
- Use `GROK_` prefix only for the four session files listed in `GROK_MEMORY.md`.
- Reusable Python mechanics belong in `D:\py_libs\rag_foundation`, not duplicated in labs.

## Handoff Checklist

When ending a session or handing off:

- [ ] `GROK_CURRENT_STATE.md` reflects latest status
- [ ] New conventions or decisions recorded in `GROK_MEMORY.md` if applicable
- [ ] Runbook updated in `GROK_RUNBOOK.md` if new commands or paths were introduced