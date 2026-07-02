"""CRS 002 M2 — Bite 3: Gradio + M1 RAG (company policies).

Startup: ingest once (m1_rag_shared). Each Submit: question → RetrievalQA → answer.

Run:
  . D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
  cd D:\\Workarea\\learning\\courses\\crs_002_build_rag_applications_get_started\\lab\\python
  python 11_m2_gradio_rag.py
"""

from __future__ import annotations

import gradio as gr
from langchain_classic.chains import RetrievalQA

from m1_rag_shared import POLICIES_URL, build_chroma_from_txt, ensure_text_file, make_llm

_qa: RetrievalQA | None = None


def _build_qa() -> RetrievalQA:
    path = ensure_text_file(POLICIES_URL, "companyPolicies.txt")
    docsearch = build_chroma_from_txt(path)
    return RetrievalQA.from_chain_type(
        llm=make_llm(),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=False,
    )


def answer(question: str) -> str:
    if _qa is None:
        return "RAG chain not ready."
    q = (question or "").strip()
    if not q:
        return "Type a question about company policies."
    result = _qa.invoke(q)
    if isinstance(result, dict):
        return str(result.get("result", result))
    return str(result)


def main() -> None:
    global _qa
    print("Building RAG chain (download → Chroma) — wait for ingest OK ...")
    _qa = _build_qa()
    print("Ready. Launching Gradio ...")

    demo = gr.Interface(
        fn=answer,
        inputs=gr.Textbox(
            label="Question",
            placeholder="What is the mobile phone policy?",
            lines=2,
        ),
        outputs=gr.Textbox(label="Answer", lines=12),
        title="M2 — Policy Q&A (RAG)",
        description="Same M1 pipeline as lab 02 — now in the browser.",
        examples=[
            "What is the mobile phone policy?",
            "Can I eat in company vehicles?",
        ],
    )
    demo.launch()


if __name__ == "__main__":
    main()