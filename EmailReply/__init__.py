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


EMAIL = """HI there,
I am emailing to say that the resort weather was way to cloudy and overcast.
I wanted to write a song called 'Here comes the sun but it never came'

What should be the weather in Arizona in April?

I really hope you fix this next time.

Thanks,
George
"""
