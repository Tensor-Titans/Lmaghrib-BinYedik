from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from .llm import llm



chat_prompt_template = PromptTemplate(
    template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

          You are a usefull travel assistant, tasked with providing useful information to the user

          <|eot_id|><|start_header_id|>user<|end_header_id|>
          {input}
          \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
          """

    , input_variables=["input"],
)

chat_chain = chat_prompt_template | llm | StrOutputParser()