import chainlit as cl
from chainlit import user_session

from utils.llm import llm
from utils.main_graph import main_app
from utils.chat_chain import chat_chain
from utils.product_price_graph import product_price_app
from utils.image_search_pipline import (
    extract_information,
    format_monument_info,
    formatJson,
    image_search_prompt,
    search_image,
    upload_to_imgbb,
)


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Lmaghrib bin ydik",
            markdown_description="Your moroccan AI travel guide",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="7di rassk",
            markdown_description="I will help you not get scammed",
            icon="https://picsum.photos/250",
        ),
    ]


# On chat start
@cl.on_chat_start
async def on_chat_start():
    # Retrieve message history
    message_history = user_session.get("MESSAGE_HISTORY", [])
    chat_profile = user_session.get("chat_profile", "Lmaghrib bin ydik")
    await cl.Message(content=f"Starting chat using the {chat_profile} profile").send()

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
    chat_profile = user_session.get("chat_profile", "Lmaghrib bin ydik")
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

    if chat_profile == "Lmaghrib bin ydik":
        await handle_culture_message(msg, message_history)
    elif chat_profile == "7di rassk":
        await handle_prices_message(msg, message_history)
    else:
        await cl.Message(
            content="Unknown profile, defaulting to Lmaghrib bin ydik profile."
        ).send()
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
    imageUrl = upload_to_imgbb(images[0].path)

    # print("__________ : ",imageUrl)
    textresponse = search_image(imageUrl)

    # print("text response: ____________\n", textresponse)

    jsonOutput = extract_information(textresponse)

    # print("jsonOutput: ____________\n", jsonOutput)
    formatedText = formatJson(jsonOutput)

    chain = image_search_prompt | llm

    result = chain.invoke({"text": formatedText})

    inputs = {"location": result}
    value = main_app.invoke(inputs)

    value = (
        value["generation"][-1]
        if type(value["generation"]) == list
        else value["generation"]
    )

    print("Value : ", value)
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

    inputs = {"question": user_text, "history": message_history}
    result = product_price_app.invoke(inputs)

    message_history.append("User: " + user_text)
    message_history.append("Assistant: " + result["generation"])
    user_session.set("MESSAGE_HISTORY", message_history)

    await cl.Message(content=result["generation"]).send()


# Run the Chainlit app
if __name__ == "__main__":
    cl.run()
