# AI Research Agent

An AI-powered research assistant that searches the web and Wikipedia, compiles structured answers, and saves results for future reference — all using **free** AI models via OpenRouter.

## Features

- 🔍 **Web search** via DuckDuckGo for up-to-date information
- 📚 **Wikipedia lookup** with error handling
- 💾 **Auto-saves** every response to `research_output.txt`
- 🆓 **Zero cost** — uses OpenRouter's free models
- 📋 **Structured JSON output** with topic, summary, sources, tools used, and keywords
- ⏱️ **Real-time status** showing what the agent is doing

## Prerequisites

- Python 3.11+
- An [OpenRouter](https://openrouter.ai) account (free tier works)

## Setup

```bash
# 1. Clone the repo
git clone <repository-url>
cd aiAgent

# 2. Create and activate virtual environment
python -m venv env
source env/bin/activate  # Linux/Mac
# .\env\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env and add your OpenRouter API key:
# OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

## Usage

```bash
python main.py
```

You'll be prompted:

```
What do you want me to research? [your question here]
```

The agent shows its progress in real-time:

```
  Searching the web...
  Generating response...

topic='Climate Change' summary='...'
  ✅ Saved to research_output.txt
```

Results are saved to `research_output.txt` with timestamps.

## Project Structure

```
├── main.py              # Entry point — agent setup, user input, response parsing
├── tools.py             # Tool definitions (web search, Wikipedia, file save)
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── research_output.txt  # Auto-generated — saved research results
```

## Tools

| Tool | What it does |
|------|-------------|
| `DuckDuckGoSearchRun` | Searches the web for current information |
| `search_wikipedia` | Looks up topics on Wikipedia (error-proof) |
| `save_to_txt` | Saves structured responses to a file with timestamp |

## Output Format

Each response is returned as structured JSON:

```json
{
  "topic": "Climate Change",
  "summary": "...",
  "sources": ["https://..."],
  "tools_used": ["duckduckgo_search"],
  "keywords": ["climate", "global warming", ...]
}
```

## Tech Stack

- **Python** 3.11+
- **LangChain** — agent orchestration framework
- **OpenRouter** — free LLM API gateway
- **DuckDuckGo** — web search
- **Wikipedia API** — encyclopedia lookup
- **Pydantic** — response validation
