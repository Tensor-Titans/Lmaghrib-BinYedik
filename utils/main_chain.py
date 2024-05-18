from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from .llm import llm


main_prompt_template = PromptTemplate(
    template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

          You are an information extractor focused on historical monuments in morocco .
          If the provided a name of  specified historical monument,
          give back information information about the monument.
          give this details about the place  'name', 'location', 'built', 'architect', 'significance', 'visitor_info', 'nearby_places'
          Provide this details as a JSON with this keys 'name', 'location', 'built', 'architect', 'significance', 'visitor_info' and no preamble or explanation.
          nearby places should be a object with place name as the key, nearby places are interesting places really close to the location the tourist can check out 
          <|eot_id|><|start_header_id|>user<|end_header_id|>
          Here is the historical monument: {location}
          {document}
          \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
          """

    , input_variables=["location", "document"],
)

main_chain = main_prompt_template | llm | JsonOutputParser()