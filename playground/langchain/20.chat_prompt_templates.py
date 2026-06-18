"""Lab 20 — ChatPromptTemplate and MessagesPlaceholder (notebook string → chat section).

Covers the notebook "Chat prompt templates" and "MessagesPlaceholder" sections.
Output parsers are Lab 21.

Run set_env.ps1, then:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\20.chat_prompt_templates.py
"""

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from watson_llm import GenParams, make_watsonx_llm


def sep(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    llama_llm = make_watsonx_llm({GenParams.MAX_NEW_TOKENS: 120})

    # --- Chat prompt template (system + user with {topic}) ---
    sep("1. ChatPromptTemplate — format only (prompt.invoke)")
    joke_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Do not expand .. Just one response only."),
        ("user", "Tell me a joke about {topic}"),
    ])
    joke_input = {"topic": "cats"}
    print(joke_prompt.invoke(joke_input))

    sep("1b. ChatPromptTemplate — send to model (prompt | llm)")
    joke_chain = joke_prompt | llama_llm
    print(joke_chain.invoke(joke_input))


    # --- MessagesPlaceholder (slot a list of messages in) ---
    sep("2. MessagesPlaceholder — format only (prompt.invoke)")
    history_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. You answer only for the request given .. Do not improvise or add anything extra. Just answer the question based on the user request."),
        MessagesPlaceholder("msgs"),
    ])
    history_input = {
        "msgs": [HumanMessage(content="What is the day after Tuesday?")],
    }
    print(history_prompt.invoke(history_input))
    sep("2b. MessagesPlaceholder — send to model (prompt | llm)")
    history_chain = history_prompt | llama_llm
    print(history_chain.invoke(history_input))


if __name__ == "__main__":
    main()