import os
import ollama
from ddgs import DDGS
from config import LLM_MODEL, SYSTEM_PROMPT


# 🔍 Web Search using DDGS
def web_search(query):
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query + " best LLM models agentic workflow", max_results=5):
                results.append(r["body"])
    except Exception as e:
        print(f"[Web Search Error] {e}")
    return "\n".join(results) if results else "No web results found."


# 🤖 LLM Recommendation via Ollama
def get_recommendations(query):
    search_data = web_search(query)

    final_input = f"""
User Query:
{query}

Web Search Context:
{search_data}

Based on the query and web context above, recommend 5 LLMs best suited for this agentic workflow.
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": final_input}
        ]
    )

    # Ollama returns response["message"]["content"]
    return response["message"]["content"]


# 🧠 Parse structured response into list of dicts
def parse_response(text):
    # Split into blocks by blank line
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    data = []

    for block in blocks:
        entry = {
            "name": "",
            "description": "",
            "parameters": "",
            "features": "",
            "tool_support": "",
            "cost": "",
            "use_case": ""
        }

        for line in block.split("\n"):
            if line.startswith("Model Name:"):
                entry["name"] = line.replace("Model Name:", "").strip()
            elif line.startswith("Description:"):
                entry["description"] = line.replace("Description:", "").strip()
            elif line.startswith("Parameters:"):
                entry["parameters"] = line.replace("Parameters:", "").strip()
            elif line.startswith("Key Features:"):
                entry["features"] = line.replace("Key Features:", "").strip()
            elif line.startswith("Tool Support:"):
                entry["tool_support"] = line.replace("Tool Support:", "").strip()
            elif line.startswith("Cost:"):
                entry["cost"] = line.replace("Cost:", "").strip()
            elif line.startswith("Best Use Case:"):
                entry["use_case"] = line.replace("Best Use Case:", "").strip()

        if entry["name"]:  # skip empty blocks
            data.append(entry)

    return data