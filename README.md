# Blog Generation Agent

An agentic blog generation system built with **LangGraph** and **FastAPI**. Given a topic, it autonomously generates a creative, SEO-friendly blog title and detailed Markdown content — with optional translation to Kannada or Japanese via conditional routing.

---

## Architecture

The system uses LangGraph to define stateful, directed agent workflows. Two graph variants are supported depending on the API input:

### Topic Graph (topic only)

```
START → title_creation → content_generation → END
```

### Language Graph (topic + language)

```
START → title_creation → content_generation → route ──┬──> Kannada_translation → END
                                                       └──> Japanese_translation → END
```

---

## Project Structure

```
Blog_Generation/
├── app.py                        # FastAPI application entry point
├── langgraph.json                # LangGraph Studio configuration
├── pyproject.toml                # Project dependencies (uv)
├── .env                          # Environment variables (not committed)
└── src/
    ├── graphs/
    │   └── graph_builder.py      # LangGraph graph definitions
    ├── nodes/
    │   └── blog_nodes.py         # Node logic: title, content, translation, routing
    ├── states/
    │   └── blogstate.py          # Typed state schema (BlogState, Blog)
    └── llms/
        └── openaillm.py          # OpenAI LLM wrapper (GPT-4o-mini)
```

---

## Tech Stack

| Component | Library / Tool |
|---|---|
| Agent Framework | LangGraph >= 1.1.3 |
| LLM | OpenAI GPT-4o-mini via LangChain OpenAI |
| API Server | FastAPI + Uvicorn |
| State Schema | Pydantic v2 + TypedDict |
| Observability | LangSmith |
| Package Manager | uv |
| Python Version | >= 3.12 |

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd Blog_Generation
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
```

### 4. Run the server

```bash
python app.py
```

The API will be available at `http://localhost:8002`.

---

## API Usage

### `POST /blogs`

Generates a blog post from a topic, with optional language translation.

#### Request Body

| Field | Type | Required | Description |
|---|---|---|---|
| `topic` | string | Yes | The subject for the blog post |
| `current_language` | string | No | Target language: `"kannada"` or `"japanese"` |

#### Example — Topic only

```bash
curl -X POST http://localhost:8002/blogs \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Future of Renewable Energy"}'
```

#### Example — With translation

```bash
curl -X POST http://localhost:8002/blogs \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Future of Renewable Energy", "current_language": "kannada"}'
```

#### Response

```json
{
  "data": {
    "topic": "The Future of Renewable Energy",
    "blog": {
      "title": "Harnessing Tomorrow: The Unstoppable Rise of Renewable Energy",
      "content": "## Introduction\n..."
    },
    "current_language": "kannada"
  }
}
```

---

## Node Details

| Node | Description |
|---|---|
| `title_creation` | Prompts the LLM to generate a creative, SEO-friendly blog title in Markdown |
| `content_generation` | Generates a detailed, structured Markdown blog post for the given topic |
| `route` | Passes `current_language` from state to enable conditional branching |
| `route_decision` | Conditional edge function — routes to `Kannada_translation` or `Japanese_translation` |
| `Kannada_translation` | Translates title and content to Kannada, preserving tone and formatting |
| `Japanese_translation` | Translates title and content to Japanese, preserving tone and formatting |

---

## LangGraph Studio

This project is configured for [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) via `langgraph.json`. The `blog_generator_agent` graph (topic graph) is exposed for visual debugging and inspection.

```bash
langgraph dev
```

---

## State Schema

```python
class Blog(BaseModel):
    title: str    # Blog post title
    content: str  # Blog post body (Markdown)

class BlogState(TypedDict):
    topic: str              # Input topic
    blog: Blog              # Generated blog (title + content)
    current_language: str   # Target language for translation
```
