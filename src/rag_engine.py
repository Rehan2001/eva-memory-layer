import google.generativeai as genai
import os
from dotenv import load_dotenv
from retriever import retrieve

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_eva(question: str) -> dict:
    context_docs = retrieve(question, top_k=5)

    context = "\n".join([
        f"[Source: {d['source']}] {d['text']}"
        for d in context_docs
    ])

    prompt = f"""You are EVA, an AI assistant for ebizframe ERP system.
You help business users understand their ERP data clearly and accurately.

Use ONLY the ERP records below to answer the question.
If the answer is not in the records, say "I don't have enough data to answer that."
Always mention which department or module the data came from.

ERP Records:
{context}

Question: {question}

Answer:"""

    response = model.generate_content(prompt)
    answer = response.text

    return {
        "question": question,
        "answer":   answer,
        "sources":  context_docs
    }

if __name__ == "__main__":
    questions = [
        "Which invoices are overdue?",
        "Which stock items are below reorder level?",
        "What is the Gross Margin KPI trend?",
    ]

    for q in questions:
        print(f"\nQ: {q}")
        result = ask_eva(q)
        print(f"EVA: {result['answer']}")
        print(f"Sources: {list(set(s['source'] for s in result['sources']))}")
        print("-" * 60)