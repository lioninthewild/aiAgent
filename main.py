from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain.agents import create_agent
import os
from tools import search_tool
import json
load_dotenv()

# Response format for research questions
class ResearchResponse(BaseModel):
    topic: str
    summary:str
    sources:list[str]
    tools_used:list[str]
    keywords: list[str]


llm = ChatOpenAI(
    model="openrouter/free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    max_tokens=500, 
)

tools =[search_tool]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful research assistant. You MUST respond with valid JSON only. Use this exact format:\n"
    '{"topic": "...", "summary": "...", "sources": ["..."], "tools_used": ["..."], "keywords": ["..."]}',
)
query =input("What do you want me to research? ")
print("Thinking...", end="", flush=True)
for step in agent.stream({"messages": [{"role": "user", "content": query}]}):
    print(".", end="", flush=True)


print()
content = step["model"]["messages"][-1].content
# Strip markdown code block if present
if content.startswith("```"):
    content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
parsed = json.loads(content)
print(ResearchResponse(**parsed))