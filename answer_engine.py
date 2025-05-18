import json
import re

# Load chunks.json on import
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip().lower()

def answer_question(query, chunks, doc_filter=None, secondary=None, detailed=False):
    query = clean_text(query)
    if secondary:
        secondary = clean_text(secondary)

    matches = []
    for chunk in chunks:
        content = clean_text(chunk["content"])
        heading = clean_text(chunk.get("heading", ""))
        source = chunk.get("source", "")

        if doc_filter and source != doc_filter:
            continue

        primary_match = query in content or query in heading
        secondary_match = secondary in content or secondary in heading if secondary else False

        if detailed:
            if primary_match and (not secondary or secondary_match):
                matches.append(chunk)
        else:
            if primary_match or (secondary and secondary_match):
                matches.append(chunk)

    return matches

def get_available_sources():
    return sorted(set(chunk.get("source", "") for chunk in chunks if "source" in chunk))
