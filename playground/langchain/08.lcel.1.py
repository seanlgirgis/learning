from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from watson_llm import make_watsonx_llm

llm = make_watsonx_llm({
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.5,
})

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