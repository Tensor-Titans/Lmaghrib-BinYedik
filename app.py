import requests
import chainlit as cl
from langchain_community.llms import HuggingFaceTextGenInference
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import os
from utils.llm import llm
from utils.graph import main_app

from pprint import pprint


# Load environment variables
load_dotenv()
serpApiKey = os.getenv('serpApiKey')
hf_token = os.getenv('hf_token')
client_id = os.getenv('client_id')

# Ensure the environment variables are loaded correctly
print(f"serpApiKey: {serpApiKey}")
print(f"hf_token: {hf_token}")
print(f"client_id: {client_id}")

# Define the functions from the notebook

def upload_to_imgbb(image_path, client_id, expiration=600):
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        url = f'https://api.imgbb.com/1/upload?expiration={expiration}&key={client_id}'
        response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()['data']['url']  # Changed 'link' to 'url'
    else:
        print(f"Error: {response.status_code} - {response.json()}")
        return None

def search_image(image_url):
    serpapi_url = f"https://serpapi.com/search.json?engine=google_lens&url={image_url}&api_key={serpApiKey}"
    response = requests.get(serpapi_url)
    return response.json()

def extract_information(response_json):
    result = {
        "knowledge_graph_title": None,
        "knowledge_graph_images_titles": [],
        "visual_matches_titles": []
    }

    knowledge_graph = response_json.get("knowledge_graph", [])
    if knowledge_graph:
        result["knowledge_graph_title"] = knowledge_graph[0].get("title")
        images = knowledge_graph[0].get("images", [])
        result["knowledge_graph_images_titles"] = [image.get("title") for image in images if "title" in image]

    visual_matches = response_json.get("visual_matches", [])
    result["visual_matches_titles"] = [match.get("title") for match in visual_matches if "title" in match]

    return result
def formatJson(information):
  text = []
  if(information['knowledge_graph_title']):
    text.append(f"Llama3 please just return this: {information['knowledge_graph_title']}")
    text.append("Knowledge Graph Images Titles:")

    for title in information["knowledge_graph_images_titles"]:
      text.append(f" - {title}")

  text.append("Visual Matches Titles:")

  for title in information["visual_matches_titles"]:
    text.append(f" - {title}")

  names_string = "\n".join(text)
  return names_string


prompt = PromptTemplate(
    template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        Based on the following list, extract the name of the monument mentioned (there is only one).
        Ensure that the location  specified is in Morocco .
        always give a result and if the place is not known from the text, return ('Unknown place)
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        here is the list {text} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
          """

    , input_variables=["text"],
)
# Define the Chainlit app
def format_monument_info(monument_info: MonumentInfo) -> str:
    formatted_info = f"""
### {monument_info.name}

**Location:** {monument_info.location}

**Built:** {monument_info.built}

**Architect:** {monument_info.architect}

**Architectural style :** {monument_info.Architectural_styles}

**Significance:** {monument_info.significance}

**Visitor Info:** {monument_info.visitor_info}

**Nearby Places:**
"""
    for place in monument_info.nearby_places:
        formatted_info += f"- [{place.name}]({place.google_maps_link})\n"

    return formatted_info


@cl.on_message
async def on_message(msg: cl.Message):
    # result=""
    # if not msg.elements:
    #     # Test
    #     inputs = {"location": "Volubilis, Meknès Prefecture, Fès-Meknès, Morocco"}
    #     for output in main_app.stream(inputs):
    #         for key, value in output.items():
    #             pprint(f"Finished running: {key}:")
    #     pprint(value["generation"])
    #     await cl.Message(content=msg.content).send()
    #     return

    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    imageUrl=upload_to_imgbb(images[0].path,client_id)

    # print("__________ : ",imageUrl)
    textresponse=search_image(imageUrl)

    # print("text response: ____________\n", textresponse)

    jsonOutput=extract_information(textresponse)

    # print("jsonOutput: ____________\n", jsonOutput)
    formatedText=formatJson(jsonOutput)
    print(formatedText)

    chain = prompt | llm
    result=chain.invoke({"text": formatedText})


    # print(imageUrl)

        # Test
    inputs = {"location": result}
    value=main_app.invoke(inputs)

    value = value["generation"] [-1]  if type(value['generation'])==list else value["generation"]

    await cl.Message(content=value).send()
    return

    # await cl.Message(content=f"{result} ").send()



# Run the Chainlit app
if __name__ == "__main__":
    cl.run()
