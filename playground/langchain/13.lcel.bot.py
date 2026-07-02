from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from watson_llm import make_watsonx_llm

llm = make_watsonx_llm({
    GenParams.MAX_NEW_TOKENS: 256,
    GenParams.TEMPERATURE: 0.5,
})

role = """
    Prediction expert with deep knowlege in topic asked.
"""

tone = "engaging and immersive"

template = """
    You are an expert {role}. I have this question {question}. I would like our conversation to be {tone}.
    
    Answer:"""

prompt = PromptTemplate.from_template(template)
# Create the LCEL chain
roleplay_chain = (
    prompt
    | llm 
    | StrOutputParser()
)

# Create an interactive chat loop
while True:
    query = input("Question: ")
    
    if query.lower() in ["quit", "exit", "bye"]:
        print("Answer: Goodbye!")
        break
        
    response = roleplay_chain.invoke({"role": role, "question": query, "tone": tone})
    print("Answer: ", response)