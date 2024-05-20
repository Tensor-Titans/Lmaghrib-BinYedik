from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
# load_dotenv()
load_dotenv(dotenv_path='./.env.dev', override=True)

os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')

web_search_tool = TavilySearchResults(k=3)