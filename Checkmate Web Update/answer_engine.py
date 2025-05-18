def answer_question(question, keyword, section, chunks):
    filtered = []

    for chunk in chunks:
        if (keyword.lower() in chunk['content'].lower() or not keyword) and            (section == chunk['heading'] or not section):
            filtered.append({
                "source": chunk["source"],
                "heading": chunk["heading"],
                "content": chunk["content"]
            })

    return filtered

def get_available_sources(chunks):
    return sorted(set(chunk["source"] for chunk in chunks))
