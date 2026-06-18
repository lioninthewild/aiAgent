from langchain_community.tools import DuckDuckGoSearchRun
from datetime import datetime
from langchain_core.tools import tool

@tool
def save_to_txt(data: str, filename: str = "research_output.txt"):
    """Save the research output to a text file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"----- Research Output-----\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Research output saved to {filename} at {timestamp}"

@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about a topic."""
    import wikipedia
    try:
        results = wikipedia.search(query, results=3)
        if not results:
            return "No Wikipedia results found."
        summaries = []
        for title in results:
            try:
                page = wikipedia.page(title=title, auto_suggest=False)
                summaries.append(f"{page.title}: {page.summary[:200]}")
            except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
                continue
        return "\n\n".join(summaries) if summaries else "No Wikipedia results found."
    except Exception:
        return "No Wikipedia results found."



search_tool = DuckDuckGoSearchRun()
wiki_tool = search_wikipedia