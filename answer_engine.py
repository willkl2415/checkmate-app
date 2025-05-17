import os
import json

def load_chunks(source_dir='chunks'):
    chunks = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        for entry in data:
                            entry['source'] = os.path.splitext(file)[0]
                            chunks.append(entry)
                    except json.JSONDecodeError:
                        continue  # Skip corrupted JSON files
    return chunks

def search_documents(primary_query, secondary_keyword=None, min_length=None, selected_source=None):
    query = primary_query.lower()
    secondary = secondary_keyword.lower() if secondary_keyword else None
    results = []
    all_chunks = load_chunks()

    for chunk in all_chunks:
        content = chunk.get("content", "").lower()
        source = chunk.get("source", "")
        if query in content:
            if secondary and secondary not in content:
                continue
            if min_length and len(chunk.get("content", "")) < min_length:
                continue
            if selected_source and source != selected_source:
                continue
            results.append(chunk)

    return results

def get_available_sources(source_dir='chunks'):
    sources = set()
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.json'):
                source_name = os.path.splitext(file)[0]
                sources.add(source_name)
    return sorted(list(sources))

def answer_question(question, source=None, secondary_keyword=None, detailed_only=False):
    """
    Returns filtered document chunks that match the user's query.
    """
    min_length = 80 if detailed_only else None
    return search_documents(
        primary_query=question,
        secondary_keyword=secondary_keyword,
        min_length=min_length,
        selected_source=source
    )
