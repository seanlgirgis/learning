"""Lab 28 — embeddings: text → vectors (before Chroma).

Run set_env.ps1, then:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\28.embeddings.demo.py
"""

from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from watson_llm import make_watsonx_embeddings

embed_params = {
    EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
    EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
}
watsonx_embedding = make_watsonx_embeddings(embed_params)

texts = [
    "LangChain helps build LLM applications.",
    "Mental health care can benefit from AI assistants.",
    "Vector search finds similar meaning, not just keywords.",
]

vectors = watsonx_embedding.embed_documents(texts)
print("Vectors created:", len(vectors))
print("Dimensions:", len(vectors[0]))
print("First 5 numbers:", vectors[0][:5])