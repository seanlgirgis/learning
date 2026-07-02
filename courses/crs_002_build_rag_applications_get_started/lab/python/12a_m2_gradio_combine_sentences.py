"""CRS 002 M2 — 04.pdf page 9 exercise: combine two sentences.

Two Textbox inputs → one Textbox output.

Run:
  . D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
  cd D:\\Workarea\\learning\\courses\\crs_002_build_rag_applications_get_started\\lab\\python
  python 12a_m2_gradio_combine_sentences.py
"""

from __future__ import annotations

import gradio as gr


def combine(sentence1: str, sentence2: str) -> str:
    parts = [(sentence1 or "").strip(), (sentence2 or "").strip()]
    parts = [p for p in parts if p]
    if not parts:
        return "Type one or two sentences, then Submit."
    return " ".join(parts)


def main() -> None:
    demo = gr.Interface(
        fn=combine,
        inputs=[
            gr.Textbox(label="Sentence 1", placeholder="First sentence"),
            gr.Textbox(label="Sentence 2", placeholder="Second sentence"),
        ],
        outputs=gr.Textbox(label="Combined"),
        title="M2 — Combine sentences",
        description="04.pdf exercise after the sum calculator.",
        examples=[
            ["Hello world.", "Gradio is fast."],
            ["Retrieval finds chunks.", "The LLM writes the answer."],
        ],
    )
    demo.launch()


if __name__ == "__main__":
    main()