import json
import re

# Load chunks from JSON
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def answer_question(question, source=None, secondary_keyword=None):
    # Normalise question for case-insensitive matching
    question_lower = question.lower()

    matched_chunks = []
    for chunk in chunks:
        content_lower = chunk["content"].lower()

        # Match question keyword
        if question_lower in content_lower:
            if source and chunk.get("source") != source:
                continue
            if secondary_keyword and secondary_keyword.lower() not in content_lower:
                continue

            matched_chunks.append({
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "source": chunk.get("source", "Unknown Source"),
                "heading": chunk.get("heading", "No Heading")
            })

    return matched_chunks

def get_available_sources(chunks):
    return sorted(set(chunk["source"] for chunk in chunks if "source" in chunk))
