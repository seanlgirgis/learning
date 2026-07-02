"""M1 smoke test — same path as notebook cells 18–30 + RetrievalQA (no Jupyter).

Run from playground/langchain so watson_llm imports work:

    cd D:\\Workarea\\learning\\playground\\langchain
    python ..\\..\\courses\\crs_002_build_rag_applications_get_started\\lab\\python\\01_m1_rag_smoke.py
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

# watson_llm lives in playground/langchain
_LANGCHAIN = Path(__file__).resolve().parents[4] / "playground" / "langchain"
if str(_LANGCHAIN) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN))

from langchain_classic.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from watson_llm import make_watsonx_embeddings, make_watsonx_llm

URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "6JDbUb_L3egv_eOkouY71A.txt"
)
WORKDIR = Path(__file__).resolve().parent / "_data"
FILENAME = WORKDIR / "companyPolicies.txt"


def main() -> None:
    WORKDIR.mkdir(parents=True, exist_ok=True)
    if not FILENAME.is_file():
        print("Downloading companyPolicies.txt ...")
        urllib.request.urlretrieve(URL, FILENAME)
    else:
        print("Using cached:", FILENAME)

    loader = TextLoader(str(FILENAME), encoding="utf-8")
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = splitter.split_documents(documents)
    print("Chunks:", len(texts))

    embeddings = make_watsonx_embeddings()
    docsearch = Chroma.from_documents(texts, embeddings)
    print("Chroma ingest OK")

    llm = make_watsonx_llm()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=False,
    )
    query = "what is mobile policy?"
    answer = qa.invoke(query)
    print("Query:", query)
    print("Answer:", answer)


if __name__ == "__main__":
    main()