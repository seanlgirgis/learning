from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from watson_llm import make_watsonx_llm

llm = make_watsonx_llm({
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.5,
})

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