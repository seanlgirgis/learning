"""Lab 32 — ParentDocumentRetriever (bite by bite — you type each step).

Small child chunks for search; larger parent chunks returned for context.
Mirror: sean_langchain_lab.ipynb — Parent document retrievers section.

Bites:
  1. Imports
  2. Load PDF → document
  3. Embeddings + splitters + Chroma + InMemoryStore
  4. ParentDocumentRetriever + add_documents
  5. Child search vs parent invoke
  6. RetrievalQA imports (notebook twin — lab 31)
  7. docsearch — flat chunks for QA (not parent retriever)
  8. RetrievalQA.from_chain_type
  9. qa.invoke("what is this paper discussing?")

Run set_env.ps1 + network.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\32.parent_document_retriever.py
"""

PDF_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
)

# --- Bite 1: imports ---
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import InMemoryStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from watson_llm import make_watsonx_embeddings

# --- Bite 2: load PDF ---
loader = PyPDFLoader(PDF_URL)
document = loader.load()
print("PDF pages:", len(document))

# --- Bite 3: splitters + stores ---
embed_params = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}
watsonx_embedding = make_watsonx_embeddings(embed_params)

parent_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=20, separator="\n")
child_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=20, separator="\n")

vectorstore = Chroma(
    collection_name="split_parents",
    embedding_function=watsonx_embedding,
)
store = InMemoryStore()

print("Splitters + stores ready")

# --- Bite 4: retriever + add_documents ---
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

retriever.add_documents(document)
print("Parent IDs in store:", len(list(store.yield_keys())))

# --- Bite 5: compare child vs parent ---
sub_docs = vectorstore.similarity_search("Langchain", k=1)
print("Child chars:", len(sub_docs[0].page_content))
print("Child:", sub_docs[0].page_content[:120], "...")

retrieved_docs = retriever.invoke("Langchain")
print("Parent chars:", len(retrieved_docs[0].page_content))
print("Parent:", retrieved_docs[0].page_content[:120], "...")

# --- Bite 6: RetrievalQA imports (notebook twin — lab 31) ---
from langchain_classic.chains import RetrievalQA
from watson_llm import make_watsonx_llm

# --- Bite 7: docsearch — flat chunks for QA ---
# Notebook uses docsearch.as_retriever(), separate from ParentDocumentRetriever above.
qa_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50, separator="\n")
chunks = qa_splitter.split_documents(document)
docsearch = Chroma.from_documents(chunks, watsonx_embedding)
print("QA chunks:", len(chunks))

# --- Bite 8: RetrievalQA chain ---
llama_llm = make_watsonx_llm()
qa = RetrievalQA.from_chain_type(
    llm=llama_llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(),
    return_source_documents=False,
)
print("RetrievalQA ready")

# --- Bite 9: ask ---
query = "what is this paper discussing?"
answer = qa.invoke(query)
print("Answer:", answer)