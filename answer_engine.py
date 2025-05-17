import json
import re

def load_chunks(filepath="chunks.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def clean(text):
    return text.strip().replace("\n", " ")

def match_score(chunk, keyword, secondary=None, detailed=False):
    text = chunk["content"].lower()
    keyword = keyword.lower()
    score = 0

    if keyword in text:
        score += 10
    if secondary and secondary.lower() in text:
        score += 5
    if detailed:
        if keyword in chunk["heading"].lower():
            score += 3
        if secondary and secondary.lower() in chunk["heading"].lower():
            score += 2
    return score

def answer_question(question, source=None, secondary=None, detailed=False):
    keyword = question.strip()
    chunks = load_chunks()

    if source and source.lower() != "all":
        chunks = [c for c in chunks if c.get("source", "").lower() == source.lower()]

    matches = []
    for chunk in chunks:
        score = match_score(chunk, keyword, secondary, detailed)
        if score > 0:
            matches.append({
                "heading": chunk["heading"],
                "content": clean(chunk["content"]),
                "source": chunk.get("source", "Unknown"),
                "score": score
            })

    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:10]

def get_available_sources(filepath="chunks.json"):
    chunks = load_chunks(filepath)
    sources = sorted(set(c.get("source", "Unknown") for c in chunks))
    return sources
