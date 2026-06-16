# Learning Repository Plan

**Status:** Implemented (skeleton) — June 2026

## Core Idea

```
Provider  →  Course | Unit (canonical)  →  Path (ordered view)
```

| Layer | What | Folder |
|-------|------|--------|
| **Course** | Coursera, DataCamp | `courses/` — `crs_` for Coursera |
| **Unit** | Skills, interview prep, anything else | `units/` — `skill_`, `interview_` prefixes |
| **Path** | Tracks, certs, custom plans | `paths/` — links to course + unit IDs |

Paths never duplicate content. Catalog (`catalog/*.yaml`) registers IDs.

## Implemented Layout

```text
learning/
├── index.html                  # hub — open in browser
├── planning/
├── catalog/
│   ├── courses.yaml
│   ├── units.yaml
│   └── paths.yaml
├── courses/                    # provider courses
├── units/                      # skills, interview, ad-hoc
├── paths/                      # ordered sequences
│   ├── coursera_ibm_rag_cert/
│   └── interview_data_engineering_core/
└── shared/
    ├── templates/              # HTML templates (from StudyBook Course_starter)
    └── snippets/
```

## HTML Documentation

- Connected pages via relative links and breadcrumbs
- Templates in `shared/templates/` — course, path, unit, field guide, quick lookup
- Each course/unit: `index.html` + `study_pages/field_guide.html` (+ chapters as needed)

## StudyBook Relationship

Mature content may stay in StudyBook; register in catalog with `studybook_mirror` path. Migrate when ready.