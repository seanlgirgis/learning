"""CRS 002 M2 — Bite 1: Hello Gradio (echo).

Type in the box → click Submit → see your text come back. No RAG yet.

Run:
  . D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
  cd D:\\Workarea\\learning\\courses\\crs_002_build_rag_applications_get_started\\lab\\python
  python 09_m2_gradio_sean.py

Open the URL printed in the terminal (usually http://127.0.0.1:7860).
Ctrl+C in the terminal to stop the server.
"""

from __future__ import annotations

import gradio as gr


def echo(message: str) -> str:
    """Return whatever the user typed — proves Gradio fn → UI works."""
    text = (message or "").strip()
    if not text:
        return "Type something and click Submit."
    return f"You said: {text}"


def main() -> None:
    demo = gr.Interface(
        fn=echo,
        inputs=gr.Textbox(label="Your message", placeholder="Hello Gradio"),
        outputs=gr.Textbox(label="Echo"),
        title="M2 — Hello Gradio",
        description="Bite 1: Python function behind a browser form.",
    )
    demo.launch()


if __name__ == "__main__":
    main()