"""CRS 002 M2 — Bite 2: Gradio file upload.

Upload one or more files → see count and names. No RAG yet — proves gr.File.

Run:
  . D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
  cd D:\\Workarea\\learning\\courses\\crs_002_build_rag_applications_get_started\\lab\\python
  python 10_m2_gradio_file.py
"""

from __future__ import annotations

from pathlib import Path

import gradio as gr


def describe_uploads(files: list[str] | None) -> str:
    """Gradio passes a list of temp file paths (one per upload)."""
    if not files:
        return "Upload or drop files, then click Submit."

    lines = [f"Count: {len(files)}", ""]
    for i, path in enumerate(files, start=1):
        p = Path(path)
        size = p.stat().st_size if p.is_file() else 0
        lines.append(f"{i}. {p.name} ({size} bytes)")
    return "\n".join(lines)


def main() -> None:
    demo = gr.Interface(
        fn=describe_uploads,
        inputs=gr.File(
            label="Upload files",
            file_count="multiple",
            file_types=[".txt", ".pdf", ".md"],
        ),
        outputs=gr.Textbox(label="Summary", lines=8),
        title="M2 — File upload",
        description="Bite 2: gr.File feeds paths into your Python function.",
    )
    demo.launch()


if __name__ == "__main__":
    main()