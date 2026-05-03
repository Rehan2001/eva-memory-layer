import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from erp_loader import load_all_documents
from vector_store import build_vector_store
from retriever import retrieve
from rag_engine import ask_eva

print("=" * 60)
print("PHASE 2 — EVA RAG ENGINE TEST")
print("=" * 60)

print("\nStep 1: Building vector store from ERP data...")
build_vector_store()

print("\nStep 2: Testing retrieval...")
results = retrieve("Which invoices are overdue?", top_k=3)
print(f"Found {len(results)} relevant records")

print("\nStep 3: Asking EVA questions...\n")

questions = [
    "Which invoices are overdue?",
    "Which stock items are below reorder level?",
    "What is the Gross Margin KPI trend?",
]

for q in questions:
    print(f"Q: {q}")
    result = ask_eva(q)
    print(f"EVA: {result['answer']}")
    print(f"Sources: {list(set(s['source'] for s in result['sources']))}")
    print("-" * 60)
