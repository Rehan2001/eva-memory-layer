import chromadb
from sentence_transformers import SentenceTransformer
from erp_loader import load_all_documents

CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "erp_knowledge"

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_vector_store():
    docs = load_all_documents()

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Delete old collection if rebuilding
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(COLLECTION_NAME)

    texts = [d["text"] for d in docs]
    ids   = [d["id"]   for d in docs]
    metas = [{"source": d["source"]} for d in docs]

    print("Creating embeddings (this takes ~30 seconds first time)...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metas)
    print(f"\nVector store built with {len(docs)} records at {CHROMA_PATH}")

if __name__ == "__main__":
    build_vector_store()