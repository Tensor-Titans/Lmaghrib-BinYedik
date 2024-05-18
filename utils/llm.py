from langchain_community.llms import HuggingFaceTextGenInference
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
hf_token = os.getenv('hf_token')

llm = HuggingFaceTextGenInference(
    inference_server_url="https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct",
    server_kwargs={
        "headers": {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json",
        }
    },
)