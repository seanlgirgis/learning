"""CRS 002 M2 — Bite 7: LLM chat in Gradio (04.pdf llm_chat.py).

No RAG — proves Textbox → LLM → Textbox. Uses your local watson_llm backend.

Run:
  . D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
  cd D:\\Workarea\\learning\\courses\\crs_002_build_rag_applications_get_started\\lab\\python
  python 15_m2_gradio_llm_chat.py
"""

from __future__ import annotations

import gradio as gr

from m1_rag_shared import make_llm

_llm = make_llm()


def _answer_text(result) -> str:
    """Chat models return AIMessage — show .content only, not the full object."""
    if isinstance(result, str):
        return result.strip()
    content = getattr(result, "content", None)
    if content is not None:
        return str(content).strip()
    return str(result).strip()


def generate_response(prompt_txt: str) -> str:
    text = (prompt_txt or "").strip()
    if not text:
        return "Type a question and click Submit."
    return _answer_text(_llm.invoke(text))


def main() -> None:
    demo = gr.Interface(
        fn=generate_response,
        inputs=gr.Textbox(
            label="Input",
            lines=2,
            placeholder="Type your question here...",
        ),
        outputs=gr.Textbox(label="Output", lines=12),
        title="M2 — LLM chatbot",
        description="04.pdf: model once at import, fn calls invoke per submit.",
        examples=[
            "What is retrieval-augmented generation in one sentence?",
            "Name three Gradio input components.",
        ],
    )
    demo.launch()


if __name__ == "__main__":
    main()