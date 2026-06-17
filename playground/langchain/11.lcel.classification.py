from langchain_core.prompts import PromptTemplate
from langchain_ibm import WatsonxLLM
from langchain_core.output_parsers import StrOutputParser       

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
        GenParams.MAX_NEW_TOKENS: 256,
        GenParams.TEMPERATURE: 0.5,
    },
)

text = """
    The concert last night was an exhilarating experience with outstanding performances by all artists.
"""

categories = "Entertainment, Food and Dining, Technology, Literature, Music."

template = """
    Classify the {text} into one of the {categories}.
    
    Category:
    
"""
prompt = PromptTemplate.from_template(template)

# Create the LCEL chain
classification_chain = (
    prompt
    | llm 
    | StrOutputParser()
)

print(classification_chain.invoke({"text": text, "categories": categories}))