from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent
import os

load_dotenv()

# Response format for research questions
class ResearchResponse(BaseModel):
    topic: str
    summary:str
    sources:list[str]
    tools_used:list[str]
    keywords: list[str]

llm = ChatOpenAI(
    model="anthropic/claude-sonnet-4-6",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    max_tokens=500,                    #within the free credits
)
# parsing the response from the LLM

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt= ChatPromptTemplate.from_messages(
    [
        ("system", 
        """
        "You are a helpful research assistant. You will be given a research question and you will help generate a research paper. Answer the user's question in a concise manner providing a summary of the topic, a list of sources you used to gather information, and a list of tools you used to find the information. Make sure to use the following format for your response:\n {format_instructions}
        """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
) .partial(format_instructions=parser.get_format_instructions())    


# response = llm.invoke("What is the meaning of life?")
# print(response)
