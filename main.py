import os
from pathlib import Path
from datetime import datetime

import gradio as gr
from pydantic import BaseModel

from tools import search_tool, wiki_tool, save_tool

SAVE_FILE = "research_output.txt"

# --------- Pydantic Model ---------
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# --------- Offline Summary Function ---------
def summarize_offline(content: str) -> str:
    lines = content.split("\n")
    summary = "\n".join(lines[:6])
    return summary.strip() if summary else "No summary available."

# --------- Research Function ---------
def research_agent(topic: str):
    tools_used = []
    sources = []
    collected_content = ""

    # Wikipedia
    wiki_summary, wiki_sources = wiki_tool(topic)
    if wiki_summary:
        collected_content += wiki_summary + "\n"
        tools_used.append("wiki")
        sources.extend(wiki_sources)

    # DuckDuckGo
    search_summary, search_sources = search_tool(topic)
    if search_summary:
        collected_content += search_summary + "\n"
        tools_used.append("search")
        sources.extend(search_sources)

    # Summary
    final_summary = summarize_offline(collected_content)

    # Structured response
    response = ResearchResponse(
        topic=topic,
        summary=final_summary,
        sources=sources,
        tools_used=tools_used
    )

    # Save
    save_tool(topic, final_summary, sources, tools_used, filename=SAVE_FILE)

    # Format for display
    formatted_output = f"Topic: {response.topic}\n\n"
    formatted_output += f"Summary:\n{response.summary}\n\n"
    formatted_output += f"Sources:\n" + "\n".join(response.sources) + "\n\n"
    formatted_output += f"Tools Used: {', '.join(response.tools_used)}"

    # Read all saved research
    saved_content = Path(SAVE_FILE).read_text(encoding="utf-8") if Path(SAVE_FILE).exists() else ""

    return formatted_output, saved_content

# --------- Load saved research ---------
def load_saved_research():
    return Path(SAVE_FILE).read_text(encoding="utf-8") if Path(SAVE_FILE).exists() else ""

# --------- Gradio UI ---------
with gr.Blocks() as demo:
    gr.Markdown("# Offline AI Research Assistant")
    gr.Markdown(
        "Enter a topic and get a structured research summary using Wikipedia and DuckDuckGo. "
        "All previous research is automatically displayed below."
    )

    with gr.Row():
        topic_input = gr.Textbox(label="Enter a topic", placeholder="Type your research topic here...", lines=4)

    with gr.Row():
        summary_output = gr.Textbox(label="Research Summary", lines=15, max_lines=50)
        saved_output = gr.Textbox(label="All Saved Research", lines=15, max_lines=50)

    research_btn = gr.Button("Research")
    research_btn.click(fn=research_agent, inputs=topic_input, outputs=[summary_output, saved_output])
    demo.load(fn=load_saved_research, outputs=saved_output)

# --------- Launch ---------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    demo.launch(server_name="0.0.0.0", server_port=port)
