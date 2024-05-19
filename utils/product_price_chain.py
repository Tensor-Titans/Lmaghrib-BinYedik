from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from .llm import llm

product_price_prompt_template = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

          You are experte in moroccan product price.
          Provide accurate and up-to-date information about product prices in Moroccan dirhams.
          
          This is the your conversation history
          {history}

          <|eot_id|><|start_header_id|>user<|end_header_id|>
          Question: {question} 
          Context: {documents} 
          Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>
          """,
    input_variables=["documents", "question", "history"],
)

product_price_chain = product_price_prompt_template | llm | StrOutputParser()
