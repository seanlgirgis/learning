"""Lab 34 — Chains (bite by bite — you type each step).

Mirror: sean_langchain_lab.ipynb — Chains + Exercise 6.

Big idea:
  Chain = wire steps together. Step 2 uses step 1's output.

Two styles (same pipeline, different syntax):
  Traditional: LLMChain + SequentialChain (langchain_classic)
  Modern:      prompt | llm | parser  +  RunnablePassthrough.assign

Notebook demo pipeline:
  location → classic dish (meal) → recipe → cook time

Exercise 6 pipeline:
  review → sentiment → summary → customer response

Run set_env.ps1 before python.

Run:
    cd D:\\Workarea\\learning\\playground\\langchain
    python .\\34.chains.py

Bites:
  1.  Imports + LLM
  2.  LLMChain — location → meal
  3.  LCEL — same single step (prompt | llm | parser)
  4.  dish_chain + recipe_chain (steps 2–3 of sequential)
  5.  SequentialChain — China → meal → recipe → time
  6.  LCEL sequential — RunnablePassthrough.assign
  7.  Exercise 6 — prompt templates + sample reviews
  8.  Exercise 6 — traditional SequentialChain (sentiment → summary → response)
  9.  Exercise 6 — LCEL pipeline + test_chains()
"""

# --- Bite 1: imports + LLM ---
from pprint import pprint

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_classic.chains import LLMChain, SequentialChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from watson_llm import make_watsonx_llm

parameters = {
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.2,
}
llama_llm = make_watsonx_llm(parameters)
print("LLM ready:", type(llama_llm).__name__)

# --- Bite 2: LLMChain — location → meal ---
print("\n--- Bite 2: LLMChain ---")

location_template = """Your job is to come up with a classic dish from the area that the users suggests.
{location}
 YOUR RESPONSE:
"""

prompt_template = PromptTemplate(
    template=location_template,
    input_variables=["location"],
)

location_chain = LLMChain(
    llm=llama_llm,
    prompt=prompt_template,
    output_key="meal",
)

pprint(location_chain.invoke(input={"location": "China"}))

# --- Bite 3: LCEL single chain (same task) ---
print("\n--- Bite 3: LCEL single chain ---")

location_prompt = PromptTemplate.from_template(location_template)
location_chain_lcel = location_prompt | llama_llm | StrOutputParser()

meal_lcel = location_chain_lcel.invoke({"location": "China"})
print("LCEL meal:", meal_lcel)

# --- Bite 4: dish_chain + recipe_chain ---
print("\n--- Bite 4: dish_chain + recipe_chain ---")

dish_template = """Given a meal {meal}, give a short and simple recipe on how to make that dish at home.
 YOUR RESPONSE:
"""
dish_prompt = PromptTemplate(template=dish_template, input_variables=["meal"])
dish_chain = LLMChain(llm=llama_llm, prompt=dish_prompt, output_key="recipe")

time_template = """Given the recipe {recipe}, estimate how much time I need to cook it.
 YOUR RESPONSE:
"""
time_prompt = PromptTemplate(template=time_template, input_variables=["recipe"])
recipe_chain = LLMChain(llm=llama_llm, prompt=time_prompt, output_key="time")

print("dish_chain + recipe_chain ready")

# --- Bite 5: SequentialChain ---
print("\n--- Bite 5: SequentialChain ---")

overall_chain = SequentialChain(
    chains=[location_chain, dish_chain, recipe_chain],
    input_variables=["location"],
    output_variables=["meal", "recipe", "time"],
    verbose=True,
)

pprint(overall_chain.invoke(input={"location": "China"}))

# --- Bite 6: LCEL sequential ---
print("\n--- Bite 6: LCEL sequential ---")

dish_chain_lcel = dish_prompt | llama_llm | StrOutputParser()
time_chain_lcel = time_prompt | llama_llm | StrOutputParser()

overall_chain_lcel = (
    RunnablePassthrough.assign(
        meal=lambda x: location_chain_lcel.invoke({"location": x["location"]})
    )
    | RunnablePassthrough.assign(
        recipe=lambda x: dish_chain_lcel.invoke({"meal": x["meal"]})
    )
    | RunnablePassthrough.assign(
        time=lambda x: time_chain_lcel.invoke({"recipe": x["recipe"]})
    )
)

pprint(overall_chain_lcel.invoke({"location": "China"}))

# --- Bite 7: Exercise 6 — templates + reviews (copy from notebook starter) ---
print("\n--- Bite 7: Exercise 6 templates ---")

positive_review = """I absolutely love this coffee maker! It brews quickly and the coffee tastes amazing.
The built-in grinder saves me so much time in the morning, and the programmable timer means
I wake up to fresh coffee every day. Worth every penny and highly recommended to any coffee enthusiast."""

negative_review = """Disappointed with this laptop. It's constantly overheating after just 30 minutes of use,
and the battery life is nowhere near the 8 hours advertised - I barely get 3 hours.
The keyboard has already started sticking on several keys after just two weeks. Would not recommend to anyone."""

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

sentiment_prompt = PromptTemplate.from_template(sentiment_template)
summary_prompt = PromptTemplate.from_template(summary_template)
response_prompt = PromptTemplate.from_template(response_template)

print("Exercise 6 prompts ready")
# --- Bite 8: traditional_chain = SequentialChain([sentiment, summary, response], ...) ---
print("\n--- Bite 8: traditional review chain ---")

sentiment_chain = LLMChain(
    llm=llama_llm,
    prompt=sentiment_prompt,
    output_key="sentiment",
)

summary_chain = LLMChain(
    llm=llama_llm,
    prompt=summary_prompt,
    output_key="summary",
)

response_chain = LLMChain(
    llm=llama_llm,
    prompt=response_prompt,
    output_key="response",
)

traditional_chain = SequentialChain(
    chains=[sentiment_chain, summary_chain, response_chain],
    input_variables=["review"],
    output_variables=["sentiment", "summary", "response"],
    verbose=True,
)

print("traditional_chain ready")
# --- Bite 9: lcel_chain + test_chains(positive_review); test_chains(negative_review) ---
print("\n--- Bite 9: LCEL review chain + tests ---")

sentiment_chain_lcel = sentiment_prompt | llama_llm | StrOutputParser()
summary_chain_lcel = summary_prompt | llama_llm | StrOutputParser()
response_chain_lcel = response_prompt | llama_llm | StrOutputParser()

lcel_chain = (
    RunnablePassthrough.assign(
        sentiment=lambda x: sentiment_chain_lcel.invoke({"review": x["review"]})
    )
    | RunnablePassthrough.assign(
        summary=lambda x: summary_chain_lcel.invoke({
            "review": x["review"],
            "sentiment": x["sentiment"],
        })
    )
    | RunnablePassthrough.assign(
        response=lambda x: response_chain_lcel.invoke({
            "review": x["review"],
            "sentiment": x["sentiment"],
            "summary": x["summary"],
        })
    )
)


def test_chains(review):
    print("\n" + "=" * 50)
    print(f"TESTING WITH REVIEW:\n{review[:100]}...\n")

    print("TRADITIONAL CHAIN RESULTS:")
    trad = traditional_chain.invoke({"review": review})
    print(f"Sentiment: {trad['sentiment'][:120]}...")
    print(f"Response: {trad['response'][:200]}...")

    print("\nLCEL CHAIN RESULTS:")
    lcel = lcel_chain.invoke({"review": review})
    print(f"Sentiment: {lcel['sentiment'][:120]}...")
    print(f"Response: {lcel['response'][:200]}...")
    print("=" * 50)


test_chains(positive_review)
test_chains(negative_review)that 