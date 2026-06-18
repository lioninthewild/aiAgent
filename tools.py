from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime

search_tool = DuckDuckGoSearchRun()
