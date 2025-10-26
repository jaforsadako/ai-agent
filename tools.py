import wikipedia
from ddgs import DDGS
from datetime import datetime

# --------------- DuckDuckGo Search Tool ----------------
def search_tool(query, max_results=3):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            urls = []
            snippets = []
            for r in results:
                urls.append(r.get('href', ''))
                snippets.append(r.get('body', ''))
            combined = "\n".join(snippets)
            return combined, urls
    except Exception as e:
        return f"Error with DuckDuckGo search: {e}", []

# --------------- Wikipedia Tool ----------------
def wiki_tool(topic):
    try:
        summary = wikipedia.summary(topic, sentences=3)
        url = wikipedia.page(topic).url
        return summary, [url]
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation error: {e}", []
    except Exception as e:
        return f"Error fetching Wikipedia: {e}", []

# --------------- Save Tool ----------------
def save_tool(topic, summary, sources, tools_used, filename="research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Topic: {topic}\n")
        f.write(f"Summary: {summary}\n")
        f.write(f"Sources: {sources}\n")
        f.write(f"Tools Used: {tools_used}\n")
        f.write("-" * 50 + "\n")
    return filename
