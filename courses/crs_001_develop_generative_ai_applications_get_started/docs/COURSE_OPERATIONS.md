# Course Operations — CRS 001

Running enforcement, testing tally, and agent backlog. **Sean authorized ongoing updates** to docs, RemNote decks, and bubble maps without asking each time.

## Agent standing duties

Each training session the agent may:

1. Append `TRAINING_LOG.md` (questions, traps, Coursera scores)
2. Update **this file** tallies and backlog
3. Fix stale or wrong docs (accuracy over legacy notes)
4. Add RemNote `source_cards/` decks when gaps appear
5. Add or extend `bubbles/` maps when concepts need spatial linking
6. Link new assets from `index.html` and field guides

## Live tally

| Asset | Count | Status |
|-------|------:|--------|
| Coursera quizzes (logged) | 2 | 100% · 5 Q + 100% · 7 Q |
| RemNote decks | 9 + 1 new | `01`–`04`, `05_01`–`05_05`; **`05_06`** invoke/vocabulary added |
| RemNote cards (approx.) | ~160 + 12 | See `source_cards/README.md` |
| Bubble maps | 2 | Landscape (10) · LCEL workflow (11) |
| Local Python labs | 17 | `lab/python/01`–`13` (+ variants) |
| Study pages (HTML) | 10+ | Field guide + 3 chapters + patterns + lookup |
| Training log rows | 8 | See `TRAINING_LOG.md` |

## Enforcement checks

| Check | Rule | Last verified |
|-------|------|---------------|
| HTML links | Relative paths only | 2026-06-15 |
| Coursera URLs | Specialization + Course 1 in catalog | 2026-06-15 |
| Flask lab claim | Theory only — **no local Flask lab, not in RemNote decks** | 2026-06-15 |
| RemNote format | `>>A)` MC · `→` cloze | ongoing |
| Bubble max | ≤ 20 bubbles per map | 2026-06-15 |
| Post-quiz bridge | Coursera `format()` ↔ lab `invoke()` documented | 2026-06-15 |

## Testing rhythm (Sean)

```text
Coursera item → local lab (if any) → RemNote deck → bubble map click-through
```

Log Coursera grades in `TRAINING_LOG.md`. Re-drill `needs_repetition` rows before new modules.

## Weak spots (active)

| Concept | Status | Reinforcement |
|---------|--------|---------------|
| `.messages` vs `.output` | needs_repetition | `05_06`, lab `03`, LCEL map |
| `human` vs `user` | needs_repetition | `05_06`, deck `03` |
| `from_template` vs `from_messages` | improving → solid on drill | `05_01`, `05_06` |
| `format()` vs `invoke()` | solid on quizzes | `05_06` vocabulary bridge |

## Backlog (agent may pull without asking)

### RemNote

- [x] `05_06_invoke_and_vocabulary.md` — invoke trio, format/invoke, roles
- [ ] `05_07_coursera_quiz_reinforcement.md` — after more platform quizzes
- [ ] Module 3 theory deck (model selection only — **no Flask coding**)

### Bubble maps

- [x] Landscape + LCEL workflow
- [ ] Optional: **Invoke rules** mini-map (6–8 bubbles) if traps persist after `05_06`

### Docs

- [x] Remove stale “Flask lab PENDING” where no lab exists
- [ ] Map Coursera week → `lab/python/` file (when Sean shares week list)
- [ ] Update `COURSE_SETUP_AUDIT.md` honest status after Course 1 complete

### Catalog

- [ ] Course 2–4 Coursera URLs when Sean provides them

## Key paths

| Item | Path |
|------|------|
| Training log | `docs/TRAINING_LOG.md` |
| This operations file | `docs/COURSE_OPERATIONS.md` |
| RemNote cards | `source_cards/` |
| Bubble maps | `bubbles/outputs/` |
| Coursera Course 1 | https://www.coursera.org/learn/develop-generative-ai-applications-get-started?specialization=rag-for-generative-ai-applications |
| Specialization | https://www.coursera.org/specializations/rag-for-generative-ai-applications |