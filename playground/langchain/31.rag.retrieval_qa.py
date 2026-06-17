"""Lab 31 — RAG answer: retriever + LLM (RetrievalQA).

Retrieve relevant chunks, stuff into prompt, Watson answers.

Uses LangChain paper PDF (better topical answers than redirecting web URL).

Bites (fill together):
  1. Imports (ingest + RetrievalQA + make_llm)
  2. Load PDF + split → chunks
  3. Chroma + retriever
  4. RetrievalQA.from_chain_type(llm, retriever, chain_type="stuff")
  5. qa.invoke("what is this paper discussing?")

Run set_env.ps1 + network.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\31.rag.retrieval_qa.py
"""

PDF_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "96-FDF8f7coh0ooim7NyEQ/langchain-paper.pdf"
)

# --- Bite 1: imports ---
from langchain_classic.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from coursera_embeddings import make_embeddings
from langchain_helper import make_llm


# --- Bite 2: ingest ---
loader = PyPDFLoader(PDF_URL)
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print("Chunks:", len(chunks))


# --- Bite 3: store + retriever ---
embed_params = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}
embedding_model = make_embeddings(embed_params)
vector_store = Chroma.from_documents(chunks, embedding_model)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
print("Retriever ready")


# --- Bite 4: QA chain ---
llm = make_llm()
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False,
)
print("RetrievalQA ready")


# --- Bite 5: ask ---
query = "what is this paper discussing?"
answer = qa.invoke(query)
print("Answer:", answer)