"""Capstone 02 — Structured Review Desk: 3-step review pipeline.

Guide: capstone/capstone02.md
Lab mirror: playground/langchain/34.chains.py (bites 7–8)

Run:
    cd D:\\Workarea\\learning\\playground\\langchain\\capstone
    python capstone_02_review_desk.py

Needs: set_env.ps1 + network (3 LLM calls per review; OpenAI via watson_llm shim).
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

warnings.simplefilter("ignore", DeprecationWarning)
warnings.showwarning = lambda *args, **kwargs: None

_LANGCHAIN_ROOT = Path(__file__).resolve().parent.parent
if str(_LANGCHAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_LANGCHAIN_ROOT))

# --- Bite 1: imports ---
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_classic.chains import LLMChain, SequentialChain
from langchain_core.prompts import PromptTemplate
from watson_llm import make_watsonx_llm


# --- Bite 2: LLM params + factory ---
LLM_PARAMS = {
    GenParams.TEMPERATURE: 0.2,
    GenParams.MAX_NEW_TOKENS: 512,
}


def make_llm():
    return make_watsonx_llm(LLM_PARAMS)


# --- Bite 3: three prompt templates (Lab 34 Exercise 6) ---
def build_prompts() -> tuple[PromptTemplate, PromptTemplate, PromptTemplate]:
    sentiment_template = """Analyze the sentiment of the following product review as positive, negative, or neutral.
Provide your analysis in the format: "SENTIMENT: [positive/negative/neutral]"

Review: {review}

Your analysis:
"""

    summary_template = """Summarize the following product review into 3-5 key bullet points.
Each bullet point should be concise and capture an important aspect mentioned in the review.

Review: {review}
Sentiment: {sentiment}

Key points:
"""

    response_template = """Write a helpful response to a customer based on their product review.
If the sentiment is positive, thank them for their feedback. If negative, express understanding
and suggest a solution or next steps. Personalize based on the specific points they mentioned.

Review: {review}
Sentiment: {sentiment}
Key points: {summary}

Response to customer:
"""

    return (
        PromptTemplate.from_template(sentiment_template),
        PromptTemplate.from_template(summary_template),
        PromptTemplate.from_template(response_template),
    )


# --- Bite 4: three LLMChains with output_key ---
def build_step_chains(
    llm,
    prompts: tuple[PromptTemplate, PromptTemplate, PromptTemplate],
) -> tuple[LLMChain, LLMChain, LLMChain]:
    sentiment_prompt, summary_prompt, response_prompt = prompts
    sentiment_chain = LLMChain(
        llm=llm,
        prompt=sentiment_prompt,
        output_key="sentiment",
    )
    summary_chain = LLMChain(
        llm=llm,
        prompt=summary_prompt,
        output_key="summary",
    )
    response_chain = LLMChain(
        llm=llm,
        prompt=response_prompt,
        output_key="response",
    )
    return sentiment_chain, summary_chain, response_chain


# --- Bite 5: SequentialChain ---

def build_review_chain() -> SequentialChain:
    llm = make_llm()
    prompts = build_prompts()
    sentiment_chain, summary_chain, response_chain = build_step_chains(llm, prompts)
    return SequentialChain(
        chains=[sentiment_chain, summary_chain, response_chain],
        input_variables=["review"],
        output_variables=["sentiment", "summary", "response"],
        verbose=False,
    )

# --- Bite 6: invoke helper ---
def analyze_review(chain: SequentialChain, review: str) -> dict:
    """Run full pipeline on one review text."""
    return chain.invoke({"review": review})

# --- Bite 7: REPL ---
def run_repl(chain: SequentialChain) -> None:
    print("Review Desk (empty line or 'quit' to exit)")
    while True:
        review = input("Review: ").strip()
        if not review or review.lower() in ("quit", "exit"):
            break
        result = analyze_review(chain, review)
        print("\n--- Sentiment ---")
        print(result["sentiment"])
        print("\n--- Summary ---")
        print(result["summary"])
        print("\n--- Response ---")
        print(result["response"])
        print()


def main() -> None:
    chain = build_review_chain()
    run_repl(chain)


if __name__ == "__main__":
    main()