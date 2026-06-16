# Units

Learning material that is **not** a provider course — skills, interview prep, topic packs, work-adjacent study.

| Prefix | Use |
|--------|-----|
| `skill_` | Technical skill depth (PySpark shuffles, SQL windows, etc.) |
| `interview_` | Interview-focused bundles (stories, drills, employer-specific packs) |
| (none) | General topic packs when prefix does not fit |

## Standard layout

```text
<unit_id>/
├── index.html
├── README.md
├── study_pages/
│   └── field_guide.html
├── bubbles/      # StudyBubble maps (TerraForm style)
│   ├── bubbles.ini
│   ├── topics/
│   ├── layouts/
│   └── outputs/
├── digest/
└── lab/          # optional
```

Use `shared/templates/unit_index_template.html` for new units.

Register every unit in `catalog/units.yaml`. Paths reference unit IDs — same pattern as courses.