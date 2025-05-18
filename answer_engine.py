import re

def get_available_sources(chunks):
    return sorted(set(chunk.get("source", "") for chunk in chunks if "source" in chunk))

def answer_question(chunks, query, secondary_keyword):
    results = []

    for chunk in chunks:
        content = chunk.get("content", "")
        if query.lower() in content.lower():
            if secondary_keyword:
                if secondary_keyword.lower() in content.lower():
                    results.append({
                        "source": chunk.get("source", ""),
                        "heading": chunk.get("heading", ""),
                        "content": highlight_keywords(content, [query, secondary_keyword])
                    })
            else:
                results.append({
                    "source": chunk.get("source", ""),
                    "heading": chunk.get("heading", ""),
                    "content": highlight_keywords(content, [query])
                })

    return results

def highlight_keywords(text, keywords):
    for keyword in keywords:
        if keyword:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            text = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)
    return text
