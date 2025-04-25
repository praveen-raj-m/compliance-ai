import os
import re
import json
from pathlib import Path
import fitz  # PyMuPDF
import nltk
import ssl
from rake_nltk import Rake



# RAKE setup
rake = Rake()

# Directory paths
BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "data" / "company_policies"
OUT_DIR = BASE_DIR / "data" / "company_chunks"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def is_article_header(line):
    line = line.strip()
    return bool(
        re.match(r'^(Article|Clause|Section|CHAPTER|§)\s+\d+', line, re.IGNORECASE)
        or re.match(r'^([A-Z]\.)?\d+(\.\d+)*(\s+-?\s*[\w\(\) ]+)?$', line)
    )

def clean_line(line):
    return re.sub(r'\s+', ' ', line.strip())

def extract_keywords(text, top_k=13):
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:top_k]

def parse_pdf(path):
    doc = fitz.open(str(path))
    return "\n".join(page.get_text() for page in doc)

def chunk_text(text, source_name="CompanyPolicy", jurisdiction="Company"):
    chunks = []
    lines = text.split("\n")
    current = {"article_id": "", "title": "", "content": ""}

    for line in lines:
        print(line)
        line = clean_line(line)
        if not line:
            continue
        if is_article_header(line):
            if current["content"]:
                chunks.append(current)
            parts = line.split(" ", 2)
            article_id = parts[0]
            title = parts[1] if len(parts) > 1 else ""
            if len(parts) > 2:
                title += " " + parts[2]
            current = {
                "article_id": article_id,
                "title": title.strip(),
                "content": ""
            }
        else:
            current["content"] += " " + line

    if current["content"]:
        chunks.append(current)

    structured = []
    for i, chunk in enumerate(chunks):
        full_text = chunk["content"].strip()
        top_keywords = extract_keywords(full_text)
        structured.append({
            "id": f"{source_name.lower()}_{i}",
            "source": source_name,
            "jurisdiction": jurisdiction,
            "article_id": chunk["article_id"],
            "title": chunk["title"],
            "top_keywords": top_keywords,
            "full_text": full_text
        })
    return structured

def process_uploaded():
    for file in os.listdir(UPLOAD_DIR):
        print(file)
        if file.endswith(".pdf"):
            source = Path(file).stem
            text = parse_pdf(UPLOAD_DIR / file)
            print(f"📄 {file} → {len(text)} characters")
            structured_chunks = chunk_text(text, source_name=source)
            out_file = OUT_DIR / f"{source}.jsonl"
            with open(out_file, "w", encoding="utf-8") as f:
                for chunk in structured_chunks:
                    json.dump(chunk, f)
                    f.write("\n")
            print(f"✅ {file} → {len(structured_chunks)} company chunks")

if __name__ == "__main__":
    process_uploaded()