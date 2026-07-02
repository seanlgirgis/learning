"""Module 3 — optional Gradio UI (05.pdf app.py workaround, port 7860).

Run:
  python lab_03_icebreaker_ui.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import gradio as gr
from llama_index.core import Document, PromptTemplate, Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

import config

ROOT = Path(__file__).resolve().parent
PROFILE_PATH = ROOT / "data" / "mock_linkedin_profile.json"
_index = None


def _configure() -> None:
    Settings.llm = OpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.0)
    Settings.embed_model = OpenAIEmbedding(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )


def _get_index() -> VectorStoreIndex:
    global _index
    if _index is None:
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        doc = Document(text=json.dumps(profile), metadata={"source": "mock_linkedin"})
        nodes = SentenceSplitter(chunk_size=config.CHUNK_SIZE).get_nodes_from_documents([doc])
        _index = VectorStoreIndex(nodes, show_progress=True)
    return _index


def load_profile(use_mock: bool) -> str:
    if not use_mock:
        return "Local lab only supports mock data (Proxycurl discontinued)."
    _configure()
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    _get_index()
    return f"Loaded: {profile['full_name']} — {profile['headline']}"


def show_facts(use_mock: bool) -> str:
    if not use_mock:
        return "Enable mock data first."
    _configure()
    engine = _get_index().as_query_engine(
        similarity_top_k=config.SIMILARITY_TOP_K,
        text_qa_template=PromptTemplate(config.INITIAL_FACTS_TEMPLATE),
    )
    return str(engine.query("Provide three interesting facts about this person's career or education."))


def ask(question: str, use_mock: bool) -> str:
    if not use_mock:
        return "Enable mock data first."
    q = (question or "").strip()
    if not q:
        return "Type a question."
    _configure()
    engine = _get_index().as_query_engine(
        similarity_top_k=config.SIMILARITY_TOP_K,
        text_qa_template=PromptTemplate(config.USER_QUESTION_TEMPLATE),
    )
    return str(engine.query(q))


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Run set_env.ps1 first.")

    with gr.Blocks(title="M3 Icebreaker") as app:
        gr.Markdown("## Icebreaker — mock LinkedIn profile")
        use_mock = gr.Checkbox(label="Use mock data", value=True)
        status = gr.Textbox(label="Status")
        load_btn = gr.Button("Load profile")
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