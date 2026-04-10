from core import get_recommendations, parse_response
from ollama_utils import get_local_models, display_local_models
from config import LLM_MODEL
import pandas as pd

print("=" * 60)
print("        AgentLens — LLM Discovery Assistant")
print("=" * 60)
print(f"  Using model: {LLM_MODEL}\n")

# 👤 User Input
query = input("Describe your agentic AI workflow: ").strip()
if not query:
    print("No query entered. Exiting.")
    exit()

print("\n[Search] Searching the web and querying LLM...\n")

# 🤖 Get recommendations
try:
    result = get_recommendations(query)
except Exception as e:
    print(f"[Error] Failed to get recommendations: {e}")
    exit()

# 🧠 Parse structured output
data = parse_response(result)

# 📊 Display as table
if data:
    df = pd.DataFrame(data, columns=[
        "name", "description", "parameters",
        "features", "tool_support", "cost", "use_case"
    ])
    df.columns = ["Name", "Description", "Parameters",
                  "Key Features", "Tool Support", "Cost", "Best Use Case"]

    print("\n" + "=" * 60)
    print("          LLM Recommendations")
    print("=" * 60 + "\n")

    for i, row in df.iterrows():
        print(f"  [{i+1}] {row['Name']}")
        print(f"       Description : {row['Description']}")
        print(f"       Parameters  : {row['Parameters']}")
        print(f"       Key Features: {row['Key Features']}")
        print(f"       Tool Support: {row['Tool Support']}")
        print(f"       Cost        : {row['Cost']}")
        print(f"       Best For    : {row['Best Use Case']}")
        print()

    print("\n" + "=" * 60)
    print("          Comparison Table")
    print("=" * 60 + "\n")
    print(df[["Name", "Parameters", "Tool Support", "Cost"]].to_string(index=False))
else:
    print("\n[!] Could not parse structured output. Raw response:\n")
    print(result)

# 💻 Local Models Section
print("\n" + "=" * 60)
print("          Local Models (Ollama)")
print("=" * 60 + "\n")

local_models = get_local_models()
display_local_models(local_models)

print("\n" + "=" * 60)
print("  Done. Happy building! 🚀")
print("=" * 60)
