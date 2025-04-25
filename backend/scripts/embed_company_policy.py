import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
import uuid

# === Config ===
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "company_chunks"
COLLECTION_NAME = "company_policy_temp"
MODEL_NAME = "intfloat/e5-large-v2"

# === Load model and client ===
model = SentenceTransformer(MODEL_NAME)
client = QdrantClient(host="localhost", port=6333)

# === Ensure collection ===
def ensure_collection():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        dim = model.get_sentence_embedding_dimension()
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )
        print(f"🆕 Created collection: {COLLECTION_NAME}")
    else:
        print(f"✅ Collection exists: {COLLECTION_NAME}")

# === Embed and upsert points ===
def embed_and_store(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]

    texts = [f"passage: {r['full_text']}" for r in records]
    vectors = model.encode(texts, normalize_embeddings=True)

    points = [
        PointStruct(id=str(uuid.uuid4()), vector=vec.tolist(), payload=r)
        for r, vec in zip(records, vectors)
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"🔼 Uploaded {len(points)} chunks from {filepath.name}")

# === Process all company policy chunks ===
def process_all():
    ensure_collection()
    for file in os.listdir(DATA_DIR):
        if file.endswith(".jsonl"):
            embed_and_store(DATA_DIR / file)

if __name__ == "__main__":
    process_all()