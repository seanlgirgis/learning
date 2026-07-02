"""M3 Step 12 — Gradio web UI (05.pdf app.py workaround, port 7860).

SN Labs uses Flask/app.py on port 5000 — this is the local Gradio equivalent.

Run:
  python steps/12_icebreaker_gradio.py
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gradio as gr

from lib.m3_shared import (
    answer_question,
    build_index_from_profile,
    configure_settings,
    generate_initial_facts,
    load_mock_profile,
    require_openai,
)

_index = None


def _ensure_index():
    global _index
    if _index is None:
        _index = build_index_from_profile(load_mock_profile())
    return _index


def load_profile(_use_mock: bool) -> str:
    if not _use_mock:
        return "Only mock data is supported locally (Proxycurl discontinued)."
    configure_settings()
    _ensure_index()
    profile = load_mock_profile()
    return f"Loaded mock profile: {profile.get('full_name')} — {profile.get('headline')}"


def show_facts(_use_mock: bool) -> str:
    if not _use_mock:
        return "Enable 'Use mock data' first."
    configure_settings()
    return generate_initial_facts(_ensure_index())


def ask(question: str, _use_mock: bool) -> str:
    if not _use_mock:
        return "Enable 'Use mock data' first."
    q = (question or "").strip()
    if not q:
        return "Type a question about the profile."
    configure_settings()
    return answer_question(_ensure_index(), q)


def main() -> None:
    require_openai()

    with gr.Blocks(title="M3 Icebreaker") as app:
        gr.Markdown("## Icebreaker bot — local mock (05.pdf workaround)")
        use_mock = gr.Checkbox(label="Use mock data", value=True)
        status = gr.Textbox(label="Status")
        load_btn = gr.Button("Load mock profile")
        facts_btn = gr.Button("Generate 3 facts")
        facts_out = gr.Textbox(label="Facts", lines=8)
        question = gr.Textbox(label="Question", lines=2)
        ask_btn = gr.Button("Ask")
        answer = gr.Textbox(label="Answer", lines=10)

        load_btn.click(load_profile, inputs=use_mock, outputs=status)
        facts_btn.click(show_facts, inputs=use_mock, outputs=facts_out)
        ask_btn.click(ask, inputs=[question, use_mock], outputs=answer)

    app.launch()


if __name__ == "__main__":
    main()