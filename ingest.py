import os
import re

def load_documents(directory="chunks"):
    """
    Loads and structures all .txt files from the specified directory.
    Returns a list of dictionaries with 'source', 'section', and 'text' keys.
    """
    documents = []

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            source_path = os.path.join(directory, filename)
            with open(source_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split by numbered sections (e.g. 1.1, 2.3.4)
            sections = re.split(r"(?m)^\s*(\d+(?:\.\d+)+)\s+", content)
            if len(sections) < 2:
                # No section numbers found, treat as flat document
                documents.append({
                    "source": filename,
                    "section": None,
                    "text": content.strip()
                })
            else:
                # Rebuild sections from matches
                for i in range(1, len(sections) - 1, 2):
                    section = sections[i]
                    text = sections[i + 1].strip()
                    documents.append({
                        "source": filename,
                        "section": section,
                        "text": text
                    })

    return documents
