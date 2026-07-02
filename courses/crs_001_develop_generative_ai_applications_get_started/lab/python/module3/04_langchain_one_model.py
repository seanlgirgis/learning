"""Bite 3 — one LangChain pipe (lab auth + Granite).

Run in Cloud IDE venv (after pip install):
    pip install langchain langchain-ibm langchain-core
    python 04_langchain_one_model.py
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ibm import ChatWatsonx

WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
PROJECT_ID = "skills-network"

prompt = PromptTemplate.from_template(
    "Reply with only the answer.\nQuestion: {question}"
)

llm = ChatWatsonx(
    model_id="ibm/granite-4-h-small",
    url=WATSONX_URL,
    project_id=PROJECT_ID,
    params={"max_new_tokens": 100},
)

chain = prompt | llm | StrOutputParser()

answer = chain.invoke({"question": "What is the capital of Canada?"})
print(answer.strip())