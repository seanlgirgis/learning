"""M1 notebook Exercise 1 — load alternate practice document.

URL from notebook cell 97 (different txt from company policies).

Run:
  cd D:\\Workarea\\learning\\playground\\langchain
  python ..\\..\\courses\\crs_002_build_rag_applications_get_started\\lab\\python\\06_m1_practice_document.py
"""

from __future__ import annotations

from langchain_classic.chains import RetrievalQA

from m1_rag_shared import PRACTICE_URL, build_chroma_from_txt, ensure_text_file, make_llm

# Ask something about the doc after you skim the first lines printed below.
QUERY = "What is this document about?"


def main() -> None:
    path = ensure_text_file(PRACTICE_URL, "practiceDocument.txt")
    with path.open(encoding="utf-8") as f:
        print("First 400 chars of practice doc:\n")
        print(f.read(400), "\n...")

    docsearch = build_chroma_from_txt(path)
    llm = make_llm()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=False,
    )
    print("\nQuery:", QUERY)
    print("Answer:", qa.invoke(QUERY))


if __name__ == "__main__":
    main()