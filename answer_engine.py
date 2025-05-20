import json

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def answer_question(query, selected_document, selected_heading, show_detailed):
    query_lower = query.lower()
    results = []

    for chunk in chunks:
        if "Glossary" in chunk["heading"]:
            continue

        if selected_document and chunk["document"] != selected_document:
            continue
        if selected_heading and chunk["heading"] != selected_heading:
            continue

        text_lower = chunk["text"].lower()

        if query_lower in text_lower:
            if show_detailed:
                results.append(chunk)
            else:
                if all(k in chunk for k in ("document", "heading", "text")):
                    results.append({
                        "document": chunk["document"],
                        "heading": chunk["heading"],
                        "text": chunk["text"]
                    })

    return results
