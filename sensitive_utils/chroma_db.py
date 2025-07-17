# sensitive_utils/chroma_db.py

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import json

client = chromadb.Client()
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.get_or_create_collection("sensitive_examples", embedding_function=embedding_function)

def load_examples():
    with open("examples.json") as f:
        examples = json.load(f)

    texts = [ex["text"] for ex in examples]
    ids = [f"example_{i}" for i in range(len(examples))]
    metadatas = [{"label": ex["label"]} for ex in examples]

    collection.add(documents=texts, metadatas=metadatas, ids=ids)

def query_similar(text: str, top_k=3):
    results = collection.query(query_texts=[text], n_results=top_k)
    return results["documents"][0], results["metadatas"][0]

def add_example(sentence: str, label: str = "UNKNOWN"):
    existing = collection.query(query_texts=[sentence], n_results=1)
    if existing["documents"] and existing["documents"][0][0] == sentence:
        return  # Already present

    id = f"example_{len(collection.get()['ids']) + 1}"
    collection.add(documents=[sentence], metadatas=[{"label": label}], ids=[id])
