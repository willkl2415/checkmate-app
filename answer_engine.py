import re

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def match_chunk(chunk, query, secondary_keyword):
    content = chunk.get("content", "").lower()
    heading = chunk.get("heading", "").lower()
    source = chunk.get("source", "").lower()
    query = query.lower()
    secondary_keyword = secondary_keyword.lower()

    return query in content or query in heading or secondary_keyword in content

def answer_question(chunks, query, secondary_keyword):
    matches = [chunk for chunk in chunks if match_chunk(chunk, query, secondary_keyword)]

    if not matches:
        return [{
            "source": "No Match Found",
            "heading": "No relevant section located",
            "content": f"No content matched your query: '{query}'"
        }]

    return matches

def get_available_sources():
    import json

    try:
        with open("chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)
            return sorted(set(chunk["source"] for chunk in chunks))
    except Exception:
        return []
