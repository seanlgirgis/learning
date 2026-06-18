"""Lab 18 — show the ability to use parameters


Run set_env.ps1, then:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\18.temperature.compare.py
"""

from watson_llm import GenParams, make_watsonx_llm
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("Tell me one {adjective} joke about {topic}")
input_ = {"adjective": "funny", "topic": "cats"}  # create a dictionary to store the corresponding input to placeholders in prompt template

llama_llm = make_watsonx_llm({GenParams.MAX_NEW_TOKENS: 80})

chain = prompt | llama_llm

print(chain.invoke(input_))