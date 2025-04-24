from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, SearchParams
import numpy as np

COLLECTION_NAME = "compliance_semantic"
MODEL_NAME = "intfloat/e5-large-v2"

model = SentenceTransformer(MODEL_NAME)
client = QdrantClient(host="localhost", port=6333)

# === Query + Filter ===
def search_legal_chunks(query, top_k=8, source_filter=None):
    query_vector = model.encode(f"query: {query}", normalize_embeddings=True).tolist()

    q_filter = None
    if source_filter:
        q_filter = Filter(
            must=[FieldCondition(key="source", match=MatchValue(value=source_filter))]
        )

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
        with_vectors=False,
        query_filter=q_filter,
        search_params=SearchParams(hnsw_ef=128)
    )
    return results, query_vector

# === Keyword Booster ===
def rerank_by_keywords(results, query, weight=0.25):
    query_words = set(query.lower().split())
    reranked = []
    for r in results:
        keywords = r.payload.get("top_keywords", [])
        match_count = len(query_words.intersection(set(" ".join(keywords).lower().split())))
        bonus = weight * match_count
        reranked.append((r, r.score + bonus))
    return sorted(reranked, key=lambda x: x[1], reverse=True)

# === CLI Entry Point ===
if __name__ == "__main__":
    import sys
    query = input("🔍 Enter your compliance question: ").strip()
    source = input("📚 Filter by source...").strip() or None
    if source:
        source = source.upper().replace(" ", "_")
    print(source)
    raw_results, _ = search_legal_chunks(query, top_k=8)
    print(raw_results)
    reranked = [(r, r.score) for r in raw_results]  

    print("\n=== Top Results ===\n")
    for i, (r, score) in enumerate(reranked[:5], 1):
        payload = r.payload
        print(f"[{i}] Score: {score:.4f}")
        print(f"→ Title: {payload.get('title', '[No title]')}")
        print(f"→ Article: {payload.get('article_id')}, Source: {payload.get('source')}")
        print(f"→ Preview: {payload['full_text'][:300]}...")
        print("-" * 80)