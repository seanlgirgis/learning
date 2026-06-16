# Courses

One folder per Coursera (`crs_`) or DataCamp course.

## Standard course layout

```text
<course_id>/
├── index.html              # course front door (linked HTML hub)
├── README.md
├── study_pages/            # theory, field guides, quick lookup, self-test
├── source_cards/           # RemNote multiple-choice exports (numbered .md)
├── source_material/        # curriculum, transcripts, screenshots
├── lab/
│   ├── python/
│   └── notes/
├── docs/
├── bubbles/                # StudyBubble maps (optional)
│   ├── topics/
│   └── outputs/
└── digest/                 # optional consolidated exports
```

## Four learning layers

```text
Theory     → study_pages/
Code       → lab/
RemNote    → source_cards/
Visual map → bubbles/outputs/
```

See `planning/remnote_source_cards.md`.