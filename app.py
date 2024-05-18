from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from utils.llm import llm
from utils.graph import main_app
from utils.chat_chain import chat_chain
import chainlit as cl
import requests
from chainlit import user_session


# Load environment variables
load_dotenv()
serpApiKey = os.getenv("serpApiKey")
hf_token = os.getenv("hf_token")
client_id = os.getenv("client_id")


# Define the functions from the notebook


def upload_to_imgbb(image_path, client_id, expiration=600):
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


prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        Based on the following list, extract the name of the monument mentioned (there is only one).
        Ensure that the location  specified is in Morocco .
        always give a result and if the place is not known from the text, return ('Unknown place)
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        here is the list {text} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
          """,
    input_variables=["text"],
)


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

    for place, info in monument_info.get('nearby places', {}).items():
        place_info = info if info else "Click for location"
        formatted_info += f"- [{place}](https://www.google.com/maps/search/?api=1&query={place}) - {place_info}\n"

    return formatted_info

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Culture LLM",
            markdown_description="The underlying LLM model is **GPT-3.5**.",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="Prices LLM",
            markdown_description="The underlying LLM model is **GPT-4**.",
            icon="https://picsum.photos/250",
        ),
    ]


# On chat start
@cl.on_chat_start
async def on_chat_start():
    # Retrieve message history
    message_history = user_session.get("MESSAGE_HISTORY", [])
    chat_profile = user_session.get("chat_profile", "Culture LLM")
    await cl.Message(
        content=f"Starting chat using the {chat_profile} chat profile"
    ).send()

    # Display previous messages if any
    if message_history:
        for msg in message_history:
            await cl.Message(content=msg).send()

    user_session.set("chat_profile", chat_profile)


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


@cl.on_chat_resume
async def on_chat_resume():
    # Retrieve message history
    message_history = user_session.get("MESSAGE_HISTORY", [])
    chat_profile = user_session.get("chat_profile", "Culture LLM")
    await cl.Message(
        content=f"Resuming chat using the {chat_profile} chat profile"
    ).send()

    # Display previous messages if any
    if message_history:
        for msg in message_history:
            await cl.Message(content=msg).send()



@cl.on_message
async def on_message(msg: cl.Message):
    # Retrieve message history
    message_history = user_session.get("MESSAGE_HISTORY", [])
    chat_profile = user_session.get("chat_profile")

    if chat_profile == "Culture LLM":
        await handle_culture_message(msg, message_history)
    elif chat_profile == "Prices LLM":
        await handle_prices_message(msg, message_history)
    else:
        await cl.Message(content="Unknown profile, defaulting to Culture LLM.").send()
        await handle_culture_message(msg, message_history)



async def handle_culture_message(msg, message_history):
    # Retrieve message history
    print("message_history", message_history)
    # Retrieve Replicate client
    client = user_session.get("REPLICATE_CLIENT")

    if not msg.elements:

        inputs = {"input": msg.content, "history": message_history}
        value = chat_chain.invoke(inputs)

        await cl.Message(content=value).send()

        # Add to history
        user_text = msg.content
        message_history.append("User: " + user_text)
        message_history.append("Assistant:" + value)
        user_session.set("MESSAGE_HISTORY", message_history)

        return

    # Processing images exclusively

    images = [file for file in msg.elements if "image" in file.mime]
    imageUrl = upload_to_imgbb(images[0].path, client_id)

    # print("__________ : ",imageUrl)
    textresponse = search_image(imageUrl)

    # print("text response: ____________\n", textresponse)

    jsonOutput = extract_information(textresponse)

    # print("jsonOutput: ____________\n", jsonOutput)
    formatedText = formatJson(jsonOutput)
    chain = prompt | llm
    result = chain.invoke({"text": formatedText})

    inputs = {"location": result}
    value = main_app.invoke(inputs)

    value = (
        value["generation"][-1]
        if type(value["generation"]) == list
        else value["generation"]
    )
    formatted_info = format_monument_info(value)

    # Add to history
    user_text = msg.content
    message_history.append("User: " + result)
    message_history.append("Assistant:" + formatted_info)
    user_session.set("MESSAGE_HISTORY", message_history)




    await cl.Message(content=formatted_info).send()
    if msg.content.strip(" "):
        inputs = {"input": msg.content, "history": message_history}
        text_value = chat_chain.invoke(inputs)

    # Add to history
        user_text = msg.content
        message_history.append("User: " + user_text)
        message_history.append("Assistant:" + text_value)
        user_session.set("MESSAGE_HISTORY", message_history)
        await cl.Message(content=text_value).send()

    return


async def handle_prices_message(msg, message_history):


    user_text = msg.content
    message_history.append("User: " + user_text)
    message_history.append("Assistant: Prices LLM specific response")
    user_session.set("MESSAGE_HISTORY", message_history)

    await cl.Message(content="Prices LLM specific response").send()







# Run the Chainlit app
if __name__ == "__main__":
    cl.run()