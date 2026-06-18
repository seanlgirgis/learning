"""Lab 14b — RunnableLambda practical: 4-stage pipe + post-LLM lambda.

Part A: prompt | RunnableLambda | llm | StrOutputParser  (4 stages)
        Lambda sits AFTER prompt — receives PromptValue, caps length → str
Part B: Post-LLM fence strip (local only, no API)

Run set_env.ps1, then:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\14b.runnable_lambda.practical.py
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from watson_llm import GenParams, make_watsonx_llm

MAX_PROMPT_CHARS = 500

qa_prompt = PromptTemplate.from_template(
    "Answer using only the context below.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer in one short sentence:"
)


def cap_filled_prompt(prompt_value) -> str:
    """Step 2 of 4: PromptValue → str. Truncate noisy context, keep Question + instruction."""
    text = prompt_value.to_string()
    if len(text) <= MAX_PROMPT_CHARS:
        return text

    marker = "\n\nQuestion:"
    idx = text.find(marker)
    if idx == -1:
        return text[:MAX_PROMPT_CHARS] + "\n… [truncated]"

    head = text[:idx]
    tail = text[idx:]  # Question + "Answer in one short sentence:"
    note = "\n… [context truncated]"
    head_budget = MAX_PROMPT_CHARS - len(tail) - len(note)
    if head_budget < 50:
        return text[:MAX_PROMPT_CHARS] + "\n… [truncated]"
    return head[:head_budget] + note + tail


def strip_markdown_fences(text: str) -> str:
    """Post-LLM lambda: model wrapped answer in fences — strip to plain str."""
    t = text.strip()
    if not t.startswith("```"):
        return t
    lines = t.splitlines()
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def sep(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    sep("Part A — 4-stage chain: prompt | lambda | llm | StrOutputParser")
    llm = make_watsonx_llm({GenParams.MAX_NEW_TOKENS: 120, GenParams.TEMPERATURE: 0.2})

    chain = (
        qa_prompt
        | RunnableLambda(cap_filled_prompt)
        | llm
        | StrOutputParser()
    )
    print("chain type:", type(chain).__name__)
    print("stages: PromptTemplate → cap_filled_prompt → WatsonxLLM → StrOutputParser")
    print()

    invoke_input = {
        "question": "Which planets are rocky and solid?",
        "context": (
            "The solar system has rocky inner planets. "
            "Mercury, Venus, Earth, and Mars are rocky and solid. "
            "Jupiter and Saturn are gas giants. "
            + ("Extra noise from a huge document. " * 40)
        ),
    }
    filled = qa_prompt.invoke(invoke_input)
    full_len = len(filled.to_string())
    capped = cap_filled_prompt(filled)
    print(f"filled prompt length: {full_len} chars")
    print(f"after lambda cap:     {len(capped)} chars (max {MAX_PROMPT_CHARS})")
    print()
    print("answer:")
    print(chain.invoke(invoke_input))

    sep("Part B — post-LLM lambda (local only, no API)")
    fenced = '```\nMercury, Venus, Earth, and Mars.\n```'
    print("before:", repr(fenced))
    print("after:", repr(strip_markdown_fences(fenced)))
    print()
    print("5-stage variant:")
    print("  prompt | RunnableLambda(cap) | llm | RunnableLambda(strip) | StrOutputParser()")


if __name__ == "__main__":
    main()