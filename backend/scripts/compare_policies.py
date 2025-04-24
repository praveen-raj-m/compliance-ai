import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchParams

# === Configuration ===
BASE_DIR = Path(__file__).resolve().parents[1]
REG_DIR = BASE_DIR / "data" / "parsed_json_semantic"
COMPANY_COLLECTION = "company_policy_temp"
REG_COLLECTION = "compliance_semantic"
SIMILARITY_THRESHOLD = 0.75

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("intfloat/e5-large-v2")

def load_regulation_chunks(source_name):
    filepath = REG_DIR / f"{source_name}.jsonl"
    if not filepath.exists():
        raise FileNotFoundError(f"No parsed file found for: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def compare_chunks(reg_source):
    print(f"🔍 Comparing regulation: {reg_source}")
    reg_chunks = load_regulation_chunks(reg_source)
    uncovered = []

    for reg in reg_chunks:
        full_text = reg.get("full_text", "")
        if not full_text.strip():
            continue

        query_vector = model.encode(f"query: {full_text}", normalize_embeddings=True).tolist()

        results = client.search(
            collection_name=COMPANY_COLLECTION,
            query_vector=query_vector,
            limit=1,
            with_payload=True,
            with_vectors=False,
            search_params=SearchParams(hnsw_ef=128)
        )

        if not results or results[0].score < SIMILARITY_THRESHOLD:
            uncovered.append({
                "article_id": reg.get("article_id", ""),
                "title": reg.get("title", ""),
                "score": results[0].score if results else 0.0,
                "source": reg.get("source", ""),
                "text": full_text[:250]
            })

    return uncovered

if __name__ == "__main__":
    source = input("📚 Enter regulation to compare (e.g., GDPR, ISO27001): ").strip().upper().replace(" ", "_")

    try:
        gaps = compare_chunks(source)
        if not gaps:
            print(f"✅ Company policy covers all key articles from {source}")
        else:
            print(f"❌ Found {len(gaps)} uncovered sections in {source}:")
            for g in gaps:
                print(f"- Article {g['article_id']} ({g['title']}), Score: {g['score']:.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")