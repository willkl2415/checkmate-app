def answer_question(question, keyword, selected_section, chunks):
    query = question.strip().lower()
    keyword = keyword.strip().lower()
    filtered = []

    for chunk in chunks:
        content = chunk["content"].lower()
        section = chunk.get("section", "Unknown Section")
        if query in content and (not keyword or keyword in content):
            if selected_section == "All Sections" or section == selected_section:
                filtered.append(chunk)

    return filtered

def get_available_sections(chunks):
    sections = set()
    for chunk in chunks:
        section = chunk.get("section")
        if section:
            sections.add(section)
    return sorted(sections)
