import os
from dotenv import load_dotenv
from google import genai
from retriever import retrieve

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_eva(question: str) -> dict:
    context_docs = retrieve(question, top_k=5)

    context = "\n".join([
        f"[Source: {d['source']}] {d['text']}"
        for d in context_docs
    ])

    prompt = f"""You are EVA, an AI assistant for ebizframe ERP system.
You help business users understand their ERP data clearly and accurately.

Use ONLY the ERP records below to answer the question.
If the answer is not in the records, say: I do not have enough data to answer that.
Always mention which department or module the data came from.

ERP Records:
{context}

Question: {question}

Answer:"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return {
        "question": question,
        "answer":   response.text,
        "sources":  context_docs
    }