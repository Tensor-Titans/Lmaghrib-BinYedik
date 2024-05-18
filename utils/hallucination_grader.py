from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from .llm import llm

grader_prompt_template = PromptTemplate(

    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing whether an
    answer is useful to resolve a prompt. Give a binary score 'yes' or 'no' to indicate whether the answer is
    useful to resolve a prompt. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
     <|eot_id|><|start_header_id|>user<|end_header_id|> Here is the answer:
    \n ------- \n
    {generation}
    \n ------- \n
    Here is the prompt: {prompt} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",

    input_variables=["prompt", "generation"],
)

hallucination_grader = grader_prompt_template | llm | JsonOutputParser()