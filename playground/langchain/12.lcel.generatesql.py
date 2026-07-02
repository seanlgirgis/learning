from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from watson_llm import make_watsonx_llm

llm = make_watsonx_llm({
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.5,
})

story = """
    Retrieve the names and email addresses of all customers from the 'customers' table who have made a purchase in the last 30 days. 
    The table 'purchases' contains a column 'purchase_date'
"""

template = """
    Generate an SQL query only with no explanation or commentary based on the {description}
    
    SQL Query:
    
"""
prompt = PromptTemplate.from_template(template)
sql_generation_chain = (
    prompt
    | llm 
    | StrOutputParser()
)
print(sql_generation_chain.invoke({"description": story}))




