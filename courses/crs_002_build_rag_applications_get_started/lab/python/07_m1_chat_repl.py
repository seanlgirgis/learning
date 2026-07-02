"""M1 notebook — interactive REPL with memory (qa() wrapper pattern).

Type questions; quit / exit / bye to stop.

Run:
  cd D:\\Workarea\\learning\\playground\\langchain
  python ..\\..\\courses\\crs_002_build_rag_applications_get_started\\lab\\python\\07_m1_chat_repl.py
"""

from __future__ import annotations

from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory

from m1_rag_shared import POLICIES_URL, build_chroma_from_txt, ensure_text_file, make_llm


def run_chat() -> None:
    path = ensure_text_file(POLICIES_URL, "companyPolicies.txt")
    docsearch = build_chroma_from_txt(path)
    llm = make_llm()

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=False,
    )
    history: list[tuple[str, str]] = []

    print("Policy Q&A — type quit, exit, or bye to stop.\n")
    while True:
        query = input("Question: ").strip()
        if query.lower() in {"quit", "exit", "bye"}:
            print("Answer: Goodbye!")
            break
        if not query:
            continue
        result = chain.invoke({"question": query, "chat_history": history})
        answer = result["answer"]
        history.append((query, answer))
        print("Answer:", answer, "\n")


if __name__ == "__main__":
    run_chat()