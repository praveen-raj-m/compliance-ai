import os
import re
import json
from pathlib import Path
import fitz  # PyMuPDF



BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw_docs"
OUT_DIR = BASE_DIR / "data" / "parsed_json_semantic"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# === RAKE Setup ===
from rake_nltk import Rake
rake = Rake()  # Uses English stopwords by default

# === Header Detector (Generalized) ===
def is_article_header(line: str) -> bool:
    line = line.strip()
    return bool(
        re.match(r'^(Article|Clause|Section|CHAPTER|§)\s+\d+', line, re.IGNORECASE)
        or re.match(r'^([A-Z]\.)?\d+(\.\d+)*(\s+-?\s*[\w\(\) ]+)?$', line)
    )

# === Text Preprocessors ===
def clean_line(line: str) -> str:
    return re.sub(r'\s+', ' ', line.strip())

def extract_keywords(text: str, top_k: int = 13):
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:top_k]

def parse_pdf(path: Path) -> str:
    doc = fitz.open(str(path))
    return "\n".join(page.get_text() for page in doc)

# === Chunker ===
def chunk_text(text: str, source_name: str, jurisdiction="unspecified") -> list:
    chunks = []
    lines = text.split("\n")
    current = {"article_id": "", "title": "", "content": ""}

    for line in lines:
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

    result = []
    for i, chunk in enumerate(chunks):
        full_text = chunk["content"].strip()
        top_keywords = extract_keywords(full_text)
        result.append({
            "id": f"{source_name.lower()}_{i}",
            "source": source_name,
            "jurisdiction": jurisdiction,
            "article_id": chunk["article_id"],
            "title": chunk["title"],
            "top_keywords": top_keywords,
            "full_text": full_text
        })
    return result

# === Main Runner ===
def process_all():
    for file in os.listdir(RAW_DIR):
        if file.endswith(".pdf"):
            source = Path(file).stem
            jurisdiction = (
                "EU" if "gdpr" in source.lower()
                else "California" if "cppa" in source.lower()
                else "Global"
            )
            text = parse_pdf(RAW_DIR / file)
            chunks = chunk_text(text, source_name=source, jurisdiction=jurisdiction)
            out_file = OUT_DIR / f"{source}.jsonl"
            with open(out_file, "w", encoding="utf-8") as f:
                for chunk in chunks:
                    json.dump(chunk, f)
                    f.write("\n")
            print(f"✅ {file} → {len(chunks)} chunks")

# === Entry Point ===
if __name__ == "__main__":
    process_all()