# import os
# import json
# from tqdm import tqdm
# from pathlib import Path
# from sentence_transformers import SentenceTransformer
# from qdrant_client import QdrantClient
# from qdrant_client.http.models import VectorParams, Distance, PointStruct
# import uuid

# # === Settings ===
# BASE_DIR = Path(__file__).resolve().parents[1]
# DATA_DIR = BASE_DIR / "data" / "parsed_json"
# COLLECTION_NAME = "compliance_chunks"
# MODEL_NAME = "intfloat/e5-large-v2"

# # === Load the embedding model ===
# model = SentenceTransformer(MODEL_NAME)

# # === Connect to Qdrant ===
# client = QdrantClient(host="localhost", port=6333)

# # === Create collection if not exists ===
# def ensure_collection():
#     if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
#         dim = model.get_sentence_embedding_dimension()
#         client.recreate_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
#         )
#         print(f"🆕 Created Qdrant collection '{COLLECTION_NAME}' with dim {dim}")
#     else:
#         print(f"✅ Qdrant collection '{COLLECTION_NAME}' exists.")

# # === Embed + upsert chunks from a file ===
# def embed_and_store(filepath):
#     with open(filepath, "r", encoding="utf-8") as f:
#         lines = [json.loads(line) for line in f]

#     texts = [f"passage: {chunk['text']}" for chunk in lines]
#     ids = [str(uuid.uuid4()) for _ in lines]
#     payloads = [{k: v for k, v in chunk.items() if k != "text"} for chunk in lines]


#     vectors = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)

#     points = [
#         PointStruct(id=id_, vector=vec.tolist(), payload=payload)
#         for id_, vec, payload in zip(ids, vectors, payloads)
#     ]

#     client.upsert(collection_name=COLLECTION_NAME, points=points)
#     print(f"🔼 Upserted {len(points)} points from {os.path.basename(filepath)}")

# # === Process all .jsonl files ===
# def process_all():
#     ensure_collection()
#     for file in os.listdir(DATA_DIR):
#         if file.endswith(".jsonl"):
#             embed_and_store(DATA_DIR / file)

# # === Entry point ===
# if __name__ == "__main__":
#     process_all()

import os
import json
from pathlib import Path
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
import uuid

# === Config ===
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "parsed_json_semantic"
COLLECTION_NAME = "compliance_semantic"
MODEL_NAME = "intfloat/e5-large-v2"

# === Load Model + DB ===
model = SentenceTransformer(MODEL_NAME)
client = QdrantClient(host="localhost", port=6333)

# === Ensure Collection ===
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

# === Embed and Store ===
def embed_and_store(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]

    texts = [f"passage: {r['full_text']}" for r in records]
    ids = [str(uuid.uuid4()) for _ in records]

    vectors = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    payloads = [
        {
            "article_id": r["article_id"],
            "title": r["title"],
            "source": r["source"],
            "jurisdiction": r["jurisdiction"],
            "top_keywords": r["top_keywords"],
            "full_text": r["full_text"]
        }
        for r in records
    ]

    points = [
        PointStruct(id=id_, vector=vec.tolist(), payload=meta)
        for id_, vec, meta in zip(ids, vectors, payloads)
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"🔼 Uploaded {len(points)} chunks from {filepath.name}")

# === Entry ===
def process_all():
    ensure_collection()
    for file in os.listdir(DATA_DIR):
        if file.endswith(".jsonl"):
            embed_and_store(DATA_DIR / file)

if __name__ == "__main__":
    process_all()
