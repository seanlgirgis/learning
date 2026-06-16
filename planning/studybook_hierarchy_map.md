# StudyBook Hierarchy → Learning Repo Map

## StudyBook top level

**`StudyBook/study_maps/DataCamp/index.html`** — master hub (dark theme, linked cards)

Points to:

| Library | Index | Role |
|---------|-------|------|
| Career tracks | `career_tracks/index.html` | Role/cert playlists (numbered `01_`, `02_`, …) |
| Skill tracks | `skill_tracks/index.html` | Focused paths (SQL, AI, PySpark, …) |
| Courses | `courses/index.html` | **Canonical course packages** (reusable, stable IDs) |
| Projects | `projects/index.html` | DataCamp project packages |

**Rule from StudyBook:** Track pages own ordering; course folders are never duplicated.

## Career tracks index

**`career_tracks/index.html`** — lighter playlist index, tiers 1–4:

- Tier 1: SQL, Databricks, Power BI, Python DE
- Tier 2: AI, ML, cloud
- etc.

Each track folder links to courses — pointers only.

## Coursera / IBM Gen AI (your current work)

| StudyBook | Learning repo |
|-----------|---------------|
| `courses/crs_001` … `crs_004` | `learning/courses/crs_00x_.../` |
| `courses/index.html` (CRS section) | registered in `catalog/courses.yaml` |
| `skill_tracks/crs_rag_for_generative_ai_applications/` (legacy path view) | `paths/coursera_ibm_gen_ai_engineering/` |

**Canonical course home:** always `courses/crs_00x_...` — not the skill_track copy.

## Learning repo equivalents

```text
learning/index.html              ≈ DataCamp/index.html (smaller hub)
learning/paths/                  ≈ career_tracks + skill_tracks + certs (ordered views)
learning/courses/                ≈ courses/ (canonical packages)
learning/units/                  ≈ (no StudyBook equivalent — interview/skills)
```

## Four layers (per course, both repos)

```text
study_pages/   HTML theory
lab/           code
source_cards/  RemNote
bubbles/       StudyBubble maps
```