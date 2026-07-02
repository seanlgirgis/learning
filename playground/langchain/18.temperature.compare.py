"""Lab 18 — compare watsonx generation parameters (temperature).

Same model (WATSONX_MODEL_ID), two settings: creative (0.8) vs precise (0.1).

Run set_env.ps1, then:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\18.temperature.compare.py
"""

# Short answer: With make_watsonx_llm(), params are fixed when you build the LLM. For different temperatures, make two LLMs — don’t tweak the same object between calls.

import os

from watson_llm import GenParams, make_watsonx_llm

print("Model:", os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))
print()



llm_creative = make_watsonx_llm({GenParams.TEMPERATURE: 0.8,GenParams.MAX_NEW_TOKENS: 80})
llm_precise = make_watsonx_llm({GenParams.TEMPERATURE: 0.1,GenParams.MAX_NEW_TOKENS: 80})

prompts = [
    "Write a short poem about artificial intelligence",
    "What are the key components of a neural network?",
    "List 5 tips for effective time management",
]

for prompt in prompts:
    print("=" * 60)
    print("PROMPT:", prompt)
    print("--- creative (0.8) ---")
    print(llm_creative.invoke(prompt))
    print("--- precise (0.1) ---")
    print(llm_precise.invoke(prompt))
    print()