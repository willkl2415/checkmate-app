from difflib import SequenceMatcher

def answer_question(query, chunks, source_filter=None, secondary_filter=None, detailed=False):
    query = query.lower()
    results = []

    for chunk in chunks:
        text = chunk["content"].lower()
        if query in text:
            if source_filter and chunk["source"] != source_filter:
                continue
            if secondary_filter and secondary_filter.lower() not in text:
                continue
            results.append({
                "content": chunk["content"],
                "source": chunk["source"],
                "heading": chunk.get("heading", "N/A"),
                "chunk_id": chunk.get("chunk_id", "N/A")
            })

    if not results and not detailed:
        # Try partial match if no exact match and not in detailed mode
        for chunk in chunks:
            text = chunk["content"].lower()
            ratio = SequenceMatcher(None, query, text).ratio()
            if ratio > 0.6:
                if source_filter and chunk["source"] != source_filter:
                    continue
                if secondary_filter and secondary_filter.lower() not in text:
                    continue
                results.append({
                    "content": chunk["content"],
                    "source": chunk["source"],
                    "heading": chunk.get("heading", "N/A"),
                    "chunk_id": chunk.get("chunk_id", "N/A")
                })

    return results

def get_available_sources(chunks):
    return sorted(set(chunk.get("source", "") for chunk in chunks if "source" in chunk))
