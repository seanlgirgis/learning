"""CRS 002 M2 — Bite 8: PDF upload + RAG (06.pdf qabot.py).

Upload PDF + ask question. Rebuilds index each submit (course pattern).

Run:
  . D:\\py_venv\\rag_application_builder_foundation\\set_env.ps1
  cd D:\\Workarea\\learning\\courses\\crs_002_build_rag_applications_get_started\\lab\\python
  python 16_m2_gradio_pdf_rag.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import gradio as gr
from langchain_classic.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

_LANGCHAIN = Path(__file__).resolve().parents[4] / "playground" / "langchain"
if str(_LANGCHAIN) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN))

from m1_rag_shared import make_llm
from watson_llm import make_watsonx_embeddings


def _pdf_path(upload) -> str:
    if upload is None:
        raise ValueError("Upload a PDF first.")
    if isinstance(upload, str):
        return upload
    name = getattr(upload, "name", None)
    if name:
        return str(name)
    raise ValueError("Could not read uploaded file path.")


def document_loader(file) -> list:
    loader = PyPDFLoader(_pdf_path(file))
    return loader.load()


def text_splitter(data: list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        length_function=len,
    )
    return splitter.split_documents(data)


def vector_database(chunks: list) -> Chroma:
    embeddings = make_watsonx_embeddings()
    return Chroma.from_documents(chunks, embeddings)


def retriever(file):
    splits = document_loader(file)
    chunks = text_splitter(splits)
    vectordb = vector_database(chunks)
    return vectordb.as_retriever()


def retriever_qa(file, query: str) -> str:
    q = (query or "").strip()
    if not q:
        return "Type a question about the uploaded PDF."
    llm = make_llm()
    retriever_obj = retriever(file)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever_obj,
        return_source_documents=False,
    )
    response = qa.invoke(q)
    if isinstance(response, dict):
        return str(response.get("result", response))
    return str(response)


def main() -> None:
    demo = gr.Interface(
        fn=retriever_qa,
        inputs=[
            gr.File(
                label="Upload PDF",
                file_count="single",
                file_types=[".pdf"],
            ),
            gr.Textbox(
                label="Question",
                lines=2,
                placeholder="Ask about the PDF you uploaded...",
            ),
        ],
        outputs=gr.Textbox(label="Answer", lines=12),
        title="M2 — PDF RAG chatbot",
        description="06.pdf: File + Textbox inputs. Use a small PDF for faster ingest.",
    )
    demo.launch()


if __name__ == "__main__":
    main()