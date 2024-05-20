from langchain_community.llms import HuggingFaceTextGenInference
from dotenv import load_dotenv
import os

# Load environment variables
# load_dotenv()
load_dotenv(dotenv_path='./.env.dev', override=True)

hf_token = os.getenv('hf_token')

llm = HuggingFaceTextGenInference(
    inference_server_url="https://jrliticly0nlznb9.us-east-1.aws.endpoints.huggingface.cloud",
    server_kwargs={
        "headers": {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json",
        }
    },
)