"""Lab 27 — Exercise 3: load PDF + web, compare two splitters on PDF.

CharacterTextSplitter (300/30) vs RecursiveCharacterTextSplitter (500/50).
Notebook loads web too; comparison is on the PDF pages only.

Bites (fill together):
  1. Imports (loaders + both splitters)
  2. Load PDF → pdf_document
  3. Load web → web_document (notebook parity; not split here)
  4. Create splitter_1 and splitter_2
  5. split_documents on PDF → chunks_1, chunks_2
  6. display_document_stats() — compare counts

Needs network.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\27.exercise3.load_split.py
"""

PDF_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
)
WEB_URL = "https://python.langchain.com/v0.2/docs/introduction/"

# --- Bite 1: imports ---
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter


# --- Bite 2: PDF ---
pdf_loader = PyPDFLoader(PDF_URL)
pdf_document = pdf_loader.load()
print("PDF pages:", len(pdf_document))


# --- Bite 3: web (loaded in notebook; optional peek) ---
web_loader = WebBaseLoader(WEB_URL)
web_document = web_loader.load()
print("Web docs:", len(web_document))


# --- Bite 4: two splitters ---
splitter_1 = CharacterTextSplitter(chunk_size=300, chunk_overlap=30, separator="\n")

splitter_2 = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)

print("Splitter 1: Character 300/30")
print("Splitter 2: Recursive 500/50")


# --- Bite 5: split PDF both ways ---
chunks_1 = splitter_1.split_documents(pdf_document)
chunks_2 = splitter_2.split_documents(pdf_document)
print("Quick counts — Character:", len(chunks_1), "| Recursive:", len(chunks_2))


def display_document_stats(docs, name):
    total_chunks = len(docs)
    total_chars = sum(len(doc.page_content) for doc in docs)
    avg_chunk_size = total_chars / total_chunks if total_chunks > 0 else 0

    all_metadata_keys = set()
    for doc in docs:
        all_metadata_keys.update(doc.metadata.keys())

    print(f"\n=== {name} Statistics ===")
    print(f"Total number of chunks: {total_chunks}")
    print(f"Average chunk size: {avg_chunk_size:.2f} characters")
    print(f"Metadata keys preserved: {', '.join(sorted(all_metadata_keys))}")

    if docs:
        example_doc = docs[min(5, total_chunks - 1)]
        print("\nExample chunk:")
        print(f"Content (first 150 chars): {example_doc.page_content[:150]}...")
        print(f"Metadata: {example_doc.metadata}")
        lengths = [len(doc.page_content) for doc in docs]
        print(f"Min chunk size: {min(lengths)} characters")
        print(f"Max chunk size: {max(lengths)} characters")


display_document_stats(chunks_1, "Character 300")
display_document_stats(chunks_2, "Recursive 500")