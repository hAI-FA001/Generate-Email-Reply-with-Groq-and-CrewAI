from langchain_groq.chat_models import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun, Tool
from dotenv import load_dotenv
import os


load_dotenv()

GROQ_LLM = ChatGroq(model=os.environ['LLM_MODEL'])
search_tool = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search_tool",
    description="A search tool used to query DuckDuckGo for search results when trying to find information from the internet. Only pass a string as input.",
    func=search_tool.run
)

EMAIL = os.environ['EMAIL']