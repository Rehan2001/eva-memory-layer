import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "erp_knowledge"

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_collection(COLLECTION_NAME)

def retrieve(question: str, top_k: int = 5):
    collection = get_collection()
    query_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "text":     results["documents"][0][i],
            "source":   results["metadatas"][0][i]["source"],
            "score":    round(1 - results["distances"][0][i], 3)
        })

    return retrieved

if __name__ == "__main__":
    q = "Which invoices are overdue?"
    print(f"Question: {q}\n")
    results = retrieve(q)
    for r in results:
        print(f"[{r['source']} | score: {r['score']}] {r['text']}")