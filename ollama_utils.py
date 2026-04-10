import ollama


def get_local_models():
    """Return list of locally installed Ollama models."""
    try:
        result = ollama.list()
        # result is an object with a .models attribute (list of model objects)
        models = result.models if hasattr(result, "models") else result.get("models", [])
        return models
    except Exception as e:
        print(f"[Ollama Error] Could not fetch local models: {e}")
        return []


def display_local_models(models):
    """Pretty-print local model info to terminal."""
    if not models:
        print("  No local Ollama models found.")
        return

    for m in models:
        # Ollama model objects have .model, .size, .details attributes
        name = getattr(m, "model", None) or m.get("name", "Unknown")
        size = getattr(m, "size", None)
        details = getattr(m, "details", {})

        size_gb = f"{size / 1e9:.2f} GB" if size else "N/A"
        family = getattr(details, "family", None) or (details.get("family") if isinstance(details, dict) else "N/A")
        params = getattr(details, "parameter_size", None) or (details.get("parameter_size") if isinstance(details, dict) else "N/A")
        quant = getattr(details, "quantization_level", None) or (details.get("quantization_level") if isinstance(details, dict) else "N/A")

        print(f"  • {name}")
        print(f"    Size: {size_gb} | Family: {family} | Params: {params} | Quant: {quant}")