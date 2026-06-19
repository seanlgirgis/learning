"""Capstone 01B — Chat: load saved Chroma → answer questions.

Requires capstone_01_ingest.py (or --corpus) run first.

Shared: capstone_shared.py

Run:
    cd D:\\Workarea\\learning\\playground\\langchain\\capstone
    python capstone_01_chat.py "What is retrieval augmented generation?"
    python capstone_01_chat.py
"""

from __future__ import annotations

import sys

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from capstone_shared import CHROMA_DIR, chroma_has_data, load_vector_store
from watson_llm import make_watsonx_llm

CHAT_LLM_PARAMS = {
    GenParams.TEMPERATURE: 0.2,
    GenParams.MAX_NEW_TOKENS: 512,
}

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You answer ONE user question using ONLY information from the context that directly helps answer it.

Rules:
- Answer the user's question in a short, focused paragraph (or a short bullet list if clearer).
- Use only context that pertains to the question; ignore unrelated passages.
- Context may contain example Q&A from research papers — do NOT repeat or ask those questions.
- Do not ask follow-up questions. Do not add topics the user did not ask about.
- Context may mix relevant and irrelevant passages — use only the relevant ones.
- If none of the passages help answer the question, say briefly that the indexed papers do not cover it.

Context:
{context}

User question: {question}

Answer:""",
)

DEFAULT_QUESTION = "What is retrieval augmented generation?"


def require_chroma_data() -> None:
    if chroma_has_data():
        return
    print(f"No vector store at {CHROMA_DIR}.")
    print("Run: python capstone_01_ingest.py --corpus")
    sys.exit(1)


def build_qa_chain(vector_store) -> RetrievalQA:
    # MMR + higher k: fewer duplicate noisy chunks (e.g. DPR example Q&A tables)
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 20},
    )
    return RetrievalQA.from_chain_type(
        llm=make_watsonx_llm(CHAT_LLM_PARAMS),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_PROMPT},
        return_source_documents=False,
    )


def ask(qa: RetrievalQA, question: str) -> str:
    result = qa.invoke(question)
    if isinstance(result, dict):
        return str(result.get("result", result)).strip()
    return str(result).strip()


def main() -> None:
    require_chroma_data()
    qa = build_qa_chain(load_vector_store())

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:]).strip()
        print(ask(qa, question))
        return

    print("Capstone RAG chat (empty line or 'quit' to exit)")
    while True:
        question = input("Q: ").strip()
        if not question or question.lower() in ("quit", "exit"):
            break
        print(ask(qa, question))
        print()


if __name__ == "__main__":
    main()