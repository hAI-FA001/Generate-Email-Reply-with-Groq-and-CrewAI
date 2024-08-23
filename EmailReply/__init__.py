from langchain_groq.chat_models import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
import os


load_dotenv()

GROQ_LLM = ChatGroq(model=os.environ['LLM_MODEL'])
search_tool = DuckDuckGoSearchRun()


EMAIL = """HI there,
I am emailing to say that the resort weather was way to cloudy and overcast.
I wanted to write a song called 'Here comes the sun but it never came'

What should be the weather in Arizona in April?

I really hope you fix this next time.

Thanks,
George
"""
