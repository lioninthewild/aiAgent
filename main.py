from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain.agents import create_agent
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
    max_tokens=500,     #within the free credits
)

agent = create_agent(
    model=llm,
    tools=[],
    response_format=ResearchResponse,
)

print("Thinking...", end="", flush=True)
for step in agent.stream({"messages": [{"role": "user", "content": "What is the capital of Nepal?"}]}):
    print(".", end="", flush=True)

print()
print(step["model"]["structured_response"])