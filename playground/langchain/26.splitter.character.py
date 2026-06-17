"""Lab 26 — CharacterTextSplitter (scissors on loaded Documents).

One big page_content → many smaller Document chunks (overlap keeps context at edges).

Uses same PDF as Lab 24. Needs network for load.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\26.splitter.character.py
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

PDF_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
)

loader = PyPDFLoader(PDF_URL)
documents = loader.load()
print("Pages loaded:", len(documents))

text_splitter = CharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separator="\n",
)

chunks = text_splitter.split_documents(documents)
print("Chunks:", len(chunks))
print("--- Chunk 10 ---")
print(chunks[10].page_content)
print(chunks[10].metadata)