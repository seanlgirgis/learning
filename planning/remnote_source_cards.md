# RemNote Source Cards

RemNote exports live in each course as **`source_cards/`** — import source, not the primary study layer.

## Format (from crs_001)

Numbered Markdown files:

```text
source_cards/
  01_chapter_topic_learning_mode.md
  02_...
  05_01_prompt_and_chat_coding.md
```

Each file: multiple-choice flip cards:

```markdown
- Question text? >>A)
    - Correct answer
    - Distractor
```

`>>A)` marks the correct option (RemNote import format).

## Four layers per course

```text
Theory      → study_pages/*.html
Code        → lab/python/
RemNote     → source_cards/*.md  → import to RemNote
Bubble map  → bubbles/outputs/*.html  (optional)
```

## Rules

- Number files so import order is obvious (`01_`, `02_`, …)
- One topic or chapter per file
- Keep cards clean — no junk noise
- Primary HTML study pages stay authoritative; cards reinforce recall