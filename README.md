# AI Blog Writing Agent

A Python-based CLI tool that generates SEO-optimized blogs using the Gemini API, NewsData.io, Datamuse, and ZenQuotes.io(Quotable.io not working). It produces a Markdown blog and JSON metadata for a given topic and tone.

## Features

- **CLI Interface**: Accepts `--topic` and `--tone` arguments.
- **Context Agent**: Generates subtopics and fetches research data (news, keywords, quotes).
- **Writing Agent**: Creates a blog with an introduction, 5 sections, and conclusion.
- **SEO Agent**: Generates SEO metadata (title, meta-description, tags, reading time, URL slug).
- **Execution Agent**: Exports blog as `.md` and metadata as `.json`.
- **Smart Engineering**: Uses `asyncio`, `tenacity`, and `cachetools` for efficient API calls.

## Setup

1. Install Python 3.11.

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - Windows: `.\venv\Scripts\activate`
   - Unix: `source venv/bin/activate`

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root with:

   ```
   GOOGLE_API_KEY=your_gemini_api_key
   NEWSDATA_API_KEY=your_newsdata_api_key
   ```

## Usage

Run the CLI with a topic and tone (default: educational):

```bash
python main.py --topic "How Python is used in AI" --tone educational
```

## Output

- **Blog**: `outputs/blogs/how_python_is_used_in_ai.md`
- **Metadata**: `outputs/metadata/how_python_is_used_in_ai.json`

## Project Structure

```
ai_blog_agent/
├── agents/
│   ├── context_agent.py
│   ├── writing_agent.py
│   ├── seo_agent.py
│   ├── execution_agent.py
├── utils/
│   ├── cli.py
│   ├── api_handler.py
├── outputs/
│   ├── blogs/
│   ├── metadata/
├── main.py
├── requirements.txt
├── .env
├── README.md
```

## Dependencies

See `requirements.txt` for the full list, including:

- `google-generativeai`
- `aiohttp`
- `tenacity`
- `cachetools`
- `python-dotenv`

