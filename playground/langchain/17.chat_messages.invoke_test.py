"""Lab 17 — chat messages (System, Human, AI) with WatsonxLLM.

Run set_env.ps1, then:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\17.chat_messages.invoke_test.py
"""

from watson_llm import GenParams, make_watsonx_llm
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


llama_llm = make_watsonx_llm({GenParams.MAX_NEW_TOKENS: 80})
print('-'*150)
msg = llama_llm.invoke([
    SystemMessage(content="You are a helpful AI bot that assists a user in choosing the perfect book to read in one short sentence"),
    HumanMessage(content="I enjoy mystery novels, what should I read?"),
])
print(msg)
print('-'*150)

msg = llama_llm.invoke([
    SystemMessage(content="You are a supportive AI bot that suggests fitness activities to a user in one short sentence"),
    HumanMessage(content="I like high-intensity workouts, what should I do?"),
    AIMessage(content="You should try a CrossFit class"),
    HumanMessage(content="How often should I attend?"),
])
print(msg)
print('-'*150)
msg = llama_llm.invoke([
    HumanMessage(content="What month follows June?"),
])
print(msg)