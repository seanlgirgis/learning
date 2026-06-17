from langchain_core.prompts import PromptTemplate
from langchain_ibm import WatsonxLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

import os

import warnings

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams


# IBM SDK warnings on every call — safe to hide while learning.
# (1) Mistral is a third-party model on watsonx — license notice.
# (2) WatsonxLLM uses legacy text/generation API; ChatWatsonx uses the newer chat API.
warnings.filterwarnings("ignore", category=UserWarning, module="ibm_watsonx_ai")


llm = WatsonxLLM(
    model_id=os.environ["WATSONX_MODEL_ID"],
    url=os.environ["WATSONX_URL"],
    project_id=os.environ["WATSONX_PROJECT_ID"],
    apikey=os.environ["WATSONX_APIKEY"],
    params={
        GenParams.MAX_NEW_TOKENS: 512,
        GenParams.TEMPERATURE: 0.2,
    },
)


# Here is an example template you can use
template = """
Analyze the following product review:
"{review}"

Provide your analysis in the following format:
- Sentiment: (positive, negative, or neutral)
- Key Features Mentioned: (list the product features mentioned)
- Summary: (one-sentence summary)
"""

product_review_prompt = PromptTemplate.from_template(template)


def format_review_prompt(variables):
    return product_review_prompt.format(**variables)


review_analysis_chain = (
    RunnableLambda(format_review_prompt)
    | llm
    | StrOutputParser()
)

reviews = [
    "I love this smartphone! The camera quality is exceptional and the battery lasts all day. The only downside is that it heats up a bit during gaming.",
    "This laptop is terrible. It's slow, crashes frequently, and the keyboard stopped working after just two months. Customer service was unhelpful.",
]

for i, review in enumerate(reviews):
    print(f"==== Review #{i + 1} ====")
    result = review_analysis_chain.invoke({"review": review})
    print(result)
    print()
