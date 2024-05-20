from langchain.prompts import PromptTemplate
import requests
import urllib.parse
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv(dotenv_path='./.env.dev', override=True)
serpApiKey = os.getenv("serpApiKey")
client_id = os.getenv("client_id")


def upload_to_imgbb(image_path, expiration=600):
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        url = f"https://api.imgbb.com/1/upload?expiration={expiration}&key={client_id}"
        response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()["data"]["url"]  # Changed 'link' to 'url'
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
        "visual_matches_titles": [],
    }

    knowledge_graph = response_json.get("knowledge_graph", [])
    if knowledge_graph:
        result["knowledge_graph_title"] = knowledge_graph[0].get("title")
        images = knowledge_graph[0].get("images", [])
        result["knowledge_graph_images_titles"] = [
            image.get("title") for image in images if "title" in image
        ]

    visual_matches = response_json.get("visual_matches", [])
    result["visual_matches_titles"] = [
        match.get("title") for match in visual_matches if "title" in match
    ]

    return result


def formatJson(information):
    text = []
    if information["knowledge_graph_title"]:
        text.append(
            f"Llama3 please just return this: {information['knowledge_graph_title']}"
        )
        text.append("Knowledge Graph Images Titles:")

        for title in information["knowledge_graph_images_titles"]:
            text.append(f" - {title}")

    text.append("Visual Matches Titles:")

    for title in information["visual_matches_titles"]:
        text.append(f" - {title}")

    names_string = "\n".join(text)
    return names_string


# Define the Chainlit app
def format_monument_info(monument_info: dict) -> str:
    formatted_info = f"""
### {monument_info.get('name', 'N/A')}

**Location:** {monument_info.get('location', 'N/A')}

**Built:** {monument_info.get('built', 'N/A')}

**Architect:** {monument_info.get('architect', 'N/A')}

**Architectural style:** {monument_info.get('architectural_style', 'N/A')}

**Significance:** {monument_info.get('significance', 'N/A')}

**Visitor Info:** {monument_info.get('visitor_info', 'N/A')}

**Nearby Places:**
"""

    starting_point_encoded = urllib.parse.quote_plus(monument_info.get("name", ""))
    for place, info in monument_info.get("nearby_places", {}).items():
        destination_encoded = urllib.parse.quote_plus(place)
        place_info = info if info else "Click for location"
        formatted_info += f"- [{place}](https://www.google.com/maps/dir/{starting_point_encoded}/{destination_encoded}) : {info} \n"

    return formatted_info


image_search_prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        Based on the following list, extract the name of the monument mentioned (there is only one).
        Ensure that the location  specified is in Morocco . and also include the city or region name next to the location extracted
        always give a result and if the place is not known from the text, return ('Unknown place)
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        here is the list {text} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
          """,
    input_variables=["text"],
)
