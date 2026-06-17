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

template = """Respond with a single sentence Only:Tell me a {adjective} joke about {content}."""
prompt = PromptTemplate.from_template(template)
parser = StrOutputParser() 

#text = prompt.format(adjective="funny", content="chickens")
#print(text)
print(f"Type of prompt: {type(prompt)}")
print(f"llm type is {type(llm)}")


chain = prompt | llm   |parser
print(f"chain type is {type(chain)}")
print('-' * 120)
print(chain.invoke({"adjective": "funny", "content": "chickens"}))
print('-' * 120)
print(chain.invoke({"adjective": "sad", "content": "fish"}))