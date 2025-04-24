# import json
# from pathlib import Path
# import subprocess

# # === Paths ===
# BASE_DIR = Path(__file__).resolve().parents[1]
# COMPANY_DIR = BASE_DIR / "data" / "company_chunks"
# REG_DIR = BASE_DIR / "data" / "parsed_json_semantic"

# # === Helper: Load and summarize chunks ===
# def load_chunks(path):
#     chunks = []
#     with open(path, "r", encoding="utf-8") as f:
#         for line in f:
#             record = json.loads(line)
#             summary = f"{record.get('article_id', '')}: {record.get('title', '')} - {record.get('full_text', '')[:300]}"
#             chunks.append(summary.strip())
#     return chunks

# def build_prompt(company_chunks, regulation_chunks, reg_source):
#     company_summary = "\n".join(f"- {c}" for c in company_chunks)
#     regulation_summary = "\n".join(f"- {r}" for r in regulation_chunks)

#     return f"""
# You are a compliance and policy expert.

# Compare the COMPANY POLICY against the selected regulation ({reg_source}). Determine which regulation articles are covered in the policy and which are missing or partially addressed.

# ## COMPANY POLICY
# {company_summary}

# ## REGULATION: {reg_source}
# {regulation_summary}

# ### OUTPUT FORMAT:
# Covered:
# - Article number: ✅ Fully addressed
# - Article number: ⚠️ Partially addressed (reason)
# - Article number: ❌ Not covered

# Give a brief reasoning for each if possible.
# """

# # === Run Ollama with local LLM ===
# def query_llm(prompt, model="nous-hermes2"):
#     process = subprocess.Popen(
#         ["ollama", "run", model],
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
#     output, error = process.communicate(input=prompt)
#     return output.strip()

# if __name__ == "__main__":
#     reg_input = input("📚 Regulation to compare (e.g., GDPR, ISO27001): ").strip().upper().replace(" ", "_")
#     comp_file = next(COMPANY_DIR.glob("*.jsonl"), None)
#     reg_file = REG_DIR / f"{reg_input}.jsonl"

#     if not comp_file or not reg_file.exists():
#         if not comp_file:
#             print("❌ Company policy chunk not found. Ensure it exists.")
#         if not reg_file.exists():   
#             print(f"❌ Regulation chunk not found for {reg_input}. Ensure it exists.")
#         print("❌ Required files not found. Ensure both chunks exist.")
#         exit()

#     print("📥 Loading company and regulation chunks...")
#     company_chunks = load_chunks(comp_file)
#     regulation_chunks = load_chunks(reg_file)
#     print(company_chunks, regulation_chunks, reg_input)

#     prompt = build_prompt(company_chunks, regulation_chunks, reg_input)
#     print("\n📤 Sending prompt to local LLM...\n")

#     result = query_llm(prompt)
#     print("\n✅ LLM Response:\n")
#     print(result)


import json
from pathlib import Path
import subprocess

# === CONFIG ===
BASE_DIR = Path(__file__).resolve().parents[1]
COMPANY_DIR = BASE_DIR / "data" / "company_chunks"
REG_DIR = BASE_DIR / "data" / "parsed_json_semantic"
DEFAULT_MODEL = "nous-hermes2"
MAX_ARTICLES = 20  # Optional limit to reduce context length

def load_chunks(path, max_chunks=None):
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            entry = {
                "id": r.get("article_id", ""),
                "title": r.get("title", ""),
                "text": r.get("full_text", "")[:300],
                "keywords": ", ".join(r.get("top_keywords", [])[:5])
            }
            chunks.append(entry)
            if max_chunks and len(chunks) >= max_chunks:
                break
    return chunks

def build_prompt(company_chunks, regulation_chunks, reg_source):
    company_section = "\n\n".join(
        f"🔹 {c['title']}\n{c['text']}" for c in company_chunks
    )
    regulation_section = "\n\n".join(
        f"📜 Article {r['id']}: {r['title']}\nKeywords: {r['keywords']}" for r in regulation_chunks
    )

    return f"""
You are a compliance and risk analysis AI.

### TASK
Compare the COMPANY POLICY against the regulation {reg_source}. For each article, decide:

- Is the requirement covered by the policy? ✅ / ⚠️ / ❌
- If ❌ or ⚠️, what is the potential RISK to the organization?
- Suggest practical MITIGATION steps for each uncovered or partially covered requirement.

Be strict and specific. Do NOT say "everything is covered" unless justified.

### COMPANY POLICY
{company_section}

### REGULATION: {reg_source}
{regulation_section}

### OUTPUT FORMAT:
- Article X: ✅ Covered / ⚠️ Partial / ❌ Missing
  Risk: [short risk if partial/missing]
  Mitigation: [specific recommended fix]

Start your analysis below.
""".strip()

def query_llm(prompt, model):
    process = subprocess.Popen(
        ["ollama", "run", model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, _ = process.communicate(input=prompt)
    return output.strip()

if __name__ == "__main__":
    reg_input = input("📚 Regulation to compare (e.g., GDPR, ISO27001): ").strip().upper().replace(" ", "_")
    model = input("🤖 Model to use (e.g., nous-hermes2): ").strip() or DEFAULT_MODEL

    comp_file = next(COMPANY_DIR.glob("*.jsonl"), None)
    reg_file = REG_DIR / f"{reg_input}.jsonl"

    if not comp_file or not reg_file.exists():
        print("❌ Required files not found.")
        exit()

    print("📥 Loading chunks...")
    company_chunks = load_chunks(comp_file)
    regulation_chunks = load_chunks(reg_file, max_chunks=MAX_ARTICLES)

    prompt = build_prompt(company_chunks, regulation_chunks, reg_input)

    print("\n🚀 Querying LLM via Ollama...\n")
    response = query_llm(prompt, model)
    print("\n✅ LLM Response:\n")
    print(response)
