from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain.agents import create_agent
import os
from tools import search_tool, wiki_tool, save_to_txt
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
    max_tokens=2000,
)

tools =[search_tool,wiki_tool, save_to_txt]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful research assistant. You MUST respond with valid JSON only. Use this exact format:\n"
    '{"topic": "...", "summary": "...", "sources": ["..."], "tools_used": ["..."], "keywords": ["..."]}',
)
query =input("What do you want me to research? ")
formatted_query = (
    f"Research topic: {query}\n"
    "Respond in JSON format with fields: topic, summary, sources, tools_used, keywords."
)
for step in agent.stream({"messages": [{"role": "user", "content": formatted_query}]}):
    if "model" in step:
        msgs = step["model"]["messages"]
        last = msgs[-1]
        if last.tool_calls:
            for tc in last.tool_calls:
                name = tc["name"]
                if name == "duckduckgo_search":
                    print("  Searching the web...", flush=True)
                elif name == "search_wikipedia":
                    print("  Looking up Wikipedia...", flush=True)
                elif name == "save_to_txt":
                    print("  Saving to file...", flush=True)
        else:
            print("  Generating response...", flush=True)


print()

# Parse the response
content = step["model"]["messages"][-1].content
# Strip markdown code block if present
if content and content.startswith("```"):
    content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
try:
    parsed = json.loads(content)
    result = ResearchResponse(**parsed)
    print(result)
    save_to_txt.invoke(json.dumps(parsed, indent=2))
    print("  ✅ Saved to research_output.txt")
except (json.JSONDecodeError, TypeError) as e:
    print(f"Failed to parse response as JSON: {e}")
    print("Raw response:", content[:500])