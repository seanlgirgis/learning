"""Lab 24 — PyPDFLoader (fetch PDF from URL → list of Documents).

Each page becomes one Document (page_content + metadata).

Needs network. DeprecationWarning on langchain_community is OK for learning.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\24.loader.pdf.py
"""

from langchain_community.document_loaders import PyPDFLoader

PDF_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
)

loader = PyPDFLoader(PDF_URL)
documents = loader.load()

print("Pages loaded:", len(documents))
print("--- Page 2 snippet ---")
print(documents[1].page_content[:500])
print("--- Page 2 metadata ---")
print(documents[1].metadata)