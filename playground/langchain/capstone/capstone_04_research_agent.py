"""Capstone 04 — Research Agent: ReAct agent with RAG + calculator tools.

Guide: capstone/capstone04.md
Lab mirror: playground/langchain/35.agents.py

Run:
    cd D:\\Workarea\\learning\\playground\\langchain\\capstone
    python capstone_04_research_agent.py

Needs: set_env.ps1 + Capstone 01 ingest (chroma_01_openai) + network.

Read main() first — that is the story. Helpers below follow the same order.
"""

from __future__ import annotations

import sys
from pathlib import Path

_LANGCHAIN_ROOT = Path(__file__).resolve().parent.parent
if str(_LANGCHAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN_ROOT))

# --- imports (everything main() needs) ---
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from capstone_shared import CHROMA_DIR, chroma_has_data, load_vector_store
from watson_llm import make_watsonx_agent_llm

LLM_PARAMS = {
    GenParams.TEMPERATURE: 0.2,
    GenParams.MAX_NEW_TOKENS: 512,
}


def main() -> None:
    # 1. Capstone 01 must have run ingest first
    require_chroma()

    # 2. Open the same Chroma DB as capstone_01_chat
    store = load_vector_store()

    # 3. Tool: search those docs when the agent needs facts
    rag_tool = build_rag_tool(store)

    # 4. Tool: math (Lab 35 Exercise 7)
    calc_tool = build_calculator_tool()

    # 5. ReAct agent + executor
    executor = build_agent_executor([rag_tool, calc_tool])
    print("Agent executor ready:", [t.name for t in executor.tools])

    # 6. Smoke tests (math + RAG) — uncomment to verify routing once
    # run_smoke_tests(executor)

    # 7. REPL
    run_repl(executor)


# --- helpers (same order as main) ---


def require_chroma() -> None:
    if chroma_has_data():
        return
    print(f"No vector store at {CHROMA_DIR}.")
    print("Run: python capstone_01_ingest.py --corpus")
    sys.exit(1)


def build_rag_tool(vector_store):
    """Search Capstone 01 Chroma — same retriever settings as capstone_01_chat."""
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 20},
    )

    def search_course_docs(query: str) -> str:
        docs = retriever.invoke(query.strip())
        if not docs:
            return "No matching passages in the course index."
        parts = []
        for i, doc in enumerate(docs[:3], start=1):
            parts.append(f"[{i}] {doc.page_content.strip()}")
        return "\n\n".join(parts)

    return Tool(
        name="search_course_docs",
        func=search_course_docs,
        description=(
            "Search indexed course PDFs for facts. "
            "Input: a short question or search phrase about the material."
        ),
    )


def build_calculator_tool() -> Tool:
    """Simple math — Lab 35 Exercise 7 (agent may send messy one-line input)."""

    def _first_line(value: str) -> str:
        line = value.strip().splitlines()[0].strip()
        for sep in ("Final Answer", "Observation", "Thought:"):
            if sep in line:
                line = line.split(sep)[0].strip()
        return line

    def calculator(expression: str) -> str:
        try:
            expr = _first_line(expression)
            return f"Result: {eval(expr)}"
        except Exception as e:
            return f"Error calculating: {str(e)}. Use one line like 25+63"

    return Tool(
        name="calculator",
        func=calculator,
        description="Single math expression only, e.g. 25+63 or 15*7. One line, no words.",
    )


def make_llm():
    return make_watsonx_agent_llm(LLM_PARAMS)


REACT_PROMPT = PromptTemplate.from_template(
    """You are a research assistant who can use tools to answer questions.
You have access to these tools:

{tools}

The available tools are: {tool_names}

Follow this format:

Question: the user's question
Thought: think about what to do
Action: the tool to use, should be one of [{tool_names}]
Action Input: the input to the tool (ONE line only)
Observation: the result from the tool
Thought: I now know the final answer
Final Answer: your final answer to the user's question

Rules:
- Use search_course_docs for facts from indexed course PDFs
- Use calculator for math only; Action Input like 25+63 or 15*7 (no extra words)
- Wait for Observation before Final Answer

Question: {input}
{agent_scratchpad}
"""
)


def build_agent_executor(tools: list[Tool]) -> AgentExecutor:
    llm = make_llm()
    agent = create_react_agent(llm=llm, tools=tools, prompt=REACT_PROMPT)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=8,
    )


def run_question(executor: AgentExecutor, text: str) -> str:
    print(f"\n{'=' * 50}\nQuestion: {text}\n{'=' * 50}")
    result = executor.invoke({"input": text})
    answer = result["output"]
    print(f"\nFinal Answer: {answer}")
    return answer


def run_smoke_tests(executor: AgentExecutor) -> None:
    for question in (
        "What is 25 + 63?",
        "What is retrieval augmented generation?",
    ):
        run_question(executor, question)


def run_repl(executor: AgentExecutor) -> None:
    print("Research agent (empty line or 'quit' to exit)")
    while True:
        question = input("Q: ").strip()
        if not question or question.lower() in ("quit", "exit"):
            break
        result = executor.invoke({"input": question})
        print(result["output"])
        print()


if __name__ == "__main__":
    main()