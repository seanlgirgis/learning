"""Lab 35 — Tools & Agents (bite by bite — you type each step).

Mirror: sean_langchain_lab.ipynb — Tools and Agents + Exercise 7.

Big idea:
  Chain  = fixed steps you wire in advance.
  Agent  = LLM picks tools in a loop (ReAct: Thought → Action → Observation).

Run set_env.ps1 before python.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\35.agents.py

Bites:
  1.  Imports + LLM
  2.  Python Calculator tool (PythonREPL)
  3.  @tool search_weather + tools list
  4.  ReAct prompt template
  5.  create_react_agent + AgentExecutor
  6.  Test queries (math + weather)
  7.  Exercise 7 — calculator + format_text tools (notebook twin)

Toggle: set False to skip Bites 2–6 (faster Exercise 7 re-run).
"""

# Set True to replay notebook agent demo (Python REPL + weather).
RUN_BITES_2_6 = False

# --- Bite 1: imports + LLM ---
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_classic.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from watson_llm import make_watsonx_llm

parameters = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.2,
}
llama_llm = make_watsonx_llm(parameters)
print("LLM ready:", type(llama_llm).__name__)

if RUN_BITES_2_6:
    # --- Bite 2: Python Calculator ---
    print("\n--- Bite 2: Python Calculator ---")

    python_repl = PythonREPL()
    python_calculator = Tool(
        name="Python Calculator",
        func=python_repl.run,
        description=(
            "Useful for calculations or executing Python code. "
            "Input should be valid Python code."
        ),
    )

    print(python_calculator.invoke("a = 3; b = 1; print(a+b)"))

    # --- Bite 3: custom tool + toolkit ---
    print("\n--- Bite 3: search_weather + tools ---")

    @tool
    def search_weather(location: str):
        """Search for the current weather in the specified location."""
        return f"The weather in {location} is currently sunny and 72°F."

    tools = [python_calculator, search_weather]
    print("Tools:", [t.name for t in tools])

    # --- Bite 4: ReAct prompt ---
    print("\n--- Bite 4: ReAct prompt ---")

    prompt_template = """You are an agent who has access to the following tools:

{tools}

The available tools are: {tool_names}

To use a tool, use this format:
Thought: I need to figure out what to do
Action: tool_name
Action Input: the input to the tool

After a tool runs you will see:
Observation: result of the tool

Repeat until you can answer, then:
Thought: I know the answer
Final Answer: the final answer to the original query

Remember: Python Calculator input must be valid Python code.

Begin!

Question: {input}
{agent_scratchpad}
"""

    prompt = PromptTemplate.from_template(prompt_template)
    print("ReAct prompt ready")

    # --- Bite 5: agent + executor ---
    print("\n--- Bite 5: agent + executor ---")

    agent = create_react_agent(llm=llama_llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    print("Agent executor ready")

    # --- Bite 6: test agent ---
    print("\n--- Bite 6: test agent ---")

    result = agent_executor.invoke({"input": "What is the square root of 256?"})
    print("Final answer:", result["output"])

    queries = [
        "What's 345 * 789?",
        "What's the weather in Miami?",
    ]
    for query in queries:
        print(f"\n{'='*50}\nQUERY: {query}\n{'='*50}")
        out = agent_executor.invoke({"input": query})
        print("Final answer:", out["output"])

# --- Bite 7a: Exercise 7 tools ---
print("\n--- Bite 7a: Exercise 7 tools ---")

def _first_line(value: str) -> str:
    """ReAct output sometimes glues extra text on line 2 — keep line 1 only."""
    line = value.strip().splitlines()[0].strip()
    for sep in ("Final Answer", "Observation", "Thought:"):
        if sep in line:
            line = line.split(sep)[0].strip()
    return line


def calculator(expression: str) -> str:
    """Add, subtract, multiply, divide. Input like '2+2' or '15/3' (one line)."""
    try:
        expr = _first_line(expression)
        return f"Result: {eval(expr)}"
    except Exception as e:
        return f"Error calculating: {str(e)}. Use one line like 25+63"


def format_text(text: str) -> str:
    """Format text. Input: 'uppercase: hello world' (NOT JSON)."""
    try:
        raw = _first_line(text)
        if raw.startswith("{"):
            return "Use format uppercase: hello world — not JSON"
        if ":" not in raw:
            return f"Use format: titlecase: {raw}"
        format_type, content = raw.split(":", 1)
        format_type = format_type.strip().lower()
        content = content.strip().strip("'\"")
        if format_type == "uppercase":
            return content.upper()
        if format_type == "lowercase":
            return content.lower()
        if format_type == "titlecase":
            return content.title()
        return f"Unknown format {format_type}. Use uppercase, lowercase, or titlecase"
    except Exception as e:
        return f"Error formatting text: {str(e)}"


ex7_tools = [
    Tool(
        name="calculator",
        func=calculator,
        description="Single math expression only, e.g. 25+63 or 15*7. One line, no words.",
    ),
    Tool(
        name="format_text",
        func=format_text,
        description="Format as uppercase: hello world or titlecase: hello world. Not JSON.",
    ),
]
print("Exercise 7 tools:", [t.name for t in ex7_tools])

# --- Bite 7b
print("\n--- Bite 7b: Exercise 7 agent + tests ---")

ex7_prompt_template = """You are a helpful assistant who can use tools to help with simple tasks.
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
- calculator Action Input: 25+63 or 15*7 (no extra words)
- format_text Action Input: uppercase: hello world (not JSON)
- Wait for Observation before Final Answer

Question: {input}
{agent_scratchpad}
"""

ex7_prompt = PromptTemplate.from_template(ex7_prompt_template)
ex7_agent = create_react_agent(llm=llama_llm, tools=ex7_tools, prompt=ex7_prompt)
ex7_executor = AgentExecutor(
    agent=ex7_agent,
    tools=ex7_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=8,
)

test_questions = [
    "What is 25 + 63?",
    "Can you convert 'hello world' to uppercase?",
    "Calculate 15 * 7",
    "titlecase: langchain is awesome",
]

for question in test_questions:
    print(f"\n===== Testing: {question} =====")
    result = ex7_executor.invoke({"input": question})
    print("Final Answer:", result["output"])