import json
import re

# Load the chunks.json file into memory once when the app starts
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


def clean(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def answer_question(query, selected_doc="All", secondary_filter="", detailed=False):
    query = clean(query)
    secondary_filter = clean(secondary_filter)
    results = []

    for chunk in chunks:
        chunk_text = clean(chunk.get("text", ""))
        source = chunk.get("source", "Unknown")

        # Filter by document if selected
        if selected_doc != "All" and selected_doc != source:
            continue

        # Check primary and optional secondary keyword
        if query in chunk_text and (not secondary_filter or secondary_filter in chunk_text):
            results.append({
                "text": chunk.get("text", ""),
                "source": source,
                "section": chunk.get("section", "")
            })

    if detailed:
        return results
    else:
        return [r["text"] for r in results]


def get_available_sources():
    # List unique document sources in the dropdown
    return sorted(list(set(chunk.get("source", "Unknown") for chunk in chunks)))
