# answer_engine.py

def answer_question(query, chunks, secondary_keyword=None, detailed=False):
    if not query:
        return []

    query_lower = query.lower()
    secondary_lower = secondary_keyword.lower() if secondary_keyword else None

    filtered = []

    for chunk in chunks:
        text = chunk['content'].lower()

        # Check for primary keyword
        primary_match = query_lower in text

        # Check for secondary keyword if provided
        secondary_match = True  # Default to True if no secondary keyword
        if secondary_lower:
            secondary_match = secondary_lower in text

        if primary_match and secondary_match:
            if detailed:
                filtered.append(chunk)
            else:
                # Return a minimal version
                filtered.append({
                    "source": chunk["source"],
                    "heading": chunk["heading"]
                })

    return filtered


def get_available_sources(chunks):
    return list(sorted(set(chunk['source'] for chunk in chunks)))
