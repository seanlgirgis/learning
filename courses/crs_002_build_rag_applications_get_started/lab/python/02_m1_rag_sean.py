"""CRS 002 M1 — Sean's version (write this with Grok, step by step).

Mission: Ask a question about company policies and get an answer grounded in the doc.

Story (human terms):
  1. Get the policy document onto this machine.
  2. Read it.
  3. Cut it into bite-sized pieces.
  4. Turn each piece into numbers (embeddings) and remember them (Chroma).
  5. Ask a question — find the right pieces — let the LLM answer from those pieces.

Reference URL (Coursera source — don't guess a different file):
  https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/6JDbUb_L3egv_eOkouY71A.txt

Save locally under: lab/python/_data/companyPolicies.txt

Run from playground/langchain (so watson_llm imports work):
  cd D:\\Workarea\\learning\\playground\\langchain
  python ..\\..\\courses\\crs_002_build_rag_applications_get_started\\lab\\python\\02_m1_rag_sean.py

---
Step 1 — Get the document here (you write this part first)
"""

# Step 1: your code here
from __future__ import annotations
import sys
import urllib.request
from pathlib import Path

# watson_llm is a helper library. Include its folder in the path in order to import it.
_LANGCHAIN = Path(__file__).resolve().parents[4] / "playground" / "langchain"
if str(_LANGCHAIN) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN))

URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "6JDbUb_L3egv_eOkouY71A.txt"
)
from watson_llm import make_watsonx_embeddings, make_watsonx_llm
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA



WORKDIR = Path(__file__).resolve().parent / "_data"
FILENAME = WORKDIR / "companyPolicies.txt"

def main() -> None:
    print(f"working dir is {WORKDIR}\nfilename is {FILENAME}")
    print(f"FILENAME is of type {type(FILENAME)}")
    print(f"watson_llm path is {_LANGCHAIN}")
    WORKDIR.mkdir(parents=True, exist_ok=True)
    if not FILENAME.is_file():
        print("Downloading companyPolicies.txt ...")
        urllib.request.urlretrieve(URL, FILENAME)
    else:
        print("Using cached:", FILENAME)
    # No actual file was downloaded or size is zero, exit with error
    if not FILENAME.is_file() or FILENAME.stat().st_size == 0:
        print("Error: file is empty or missing:", FILENAME)
        return sys.exit(1)
    print(f"OK — {FILENAME.stat().st_size} bytes")
    loader = TextLoader(str(FILENAME), encoding="utf-8")
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = splitter.split_documents(documents)
    print("Chunks:", len(texts))

    embeddings = make_watsonx_embeddings()
    # Default in memory Chroma . 
    docsearch = Chroma.from_documents(texts, embeddings)
    print("Chroma ingest OK")

    llm = make_watsonx_llm()
    # Using the QA chain from langchain_classic, which is the original version of langchain. It has a different API than the newer langchain.chains.RetrievalQA, but it works fine for this demo.
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=False,
    )

    query = "Can you summarize the document for me?"
    answer = qa.invoke(query)
    print("Query:", query)
    print("Answer:", answer)    
    

if __name__ == "__main__":
    main()