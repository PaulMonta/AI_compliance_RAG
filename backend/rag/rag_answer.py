import numpy as np
import faiss
from openai import OpenAI

client = OpenAI()
CHAT_MODEL = "gpt-4o-mini"
EMBED_MODEL = "text-embedding-3-small"

def embed_query(query):
    resp = client.embeddings.create(model=EMBED_MODEL, input=query)
    vectors = [d.embedding for d in resp.data]
    vec = np.array(vectors, dtype="float32")
    faiss.normalize_L2(vec)
    return vec

def retrieve(query, index, chunks, k=4):
    qvec = embed_query(query)
    _, ids = index.search(qvec, k)
    results = []
    for i in ids[0]:
        if i != -1:
            results.append(chunks[i])

    return results

def generate_answer(user_question, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    response = client.responses.create(
        model=CHAT_MODEL,
        instructions=(
            "You are an AI compliance assistant specialized in AI regulations. "
            "You help legal, technical, and product teams understand their obligations "
            "under the EU AI Act and the NIST AI Risk Management Framework. "
            
            "Answer questions based ONLY on the provided context. "
            "If the context does not contain enough information to answer, "
            "respond: 'I could not find relevant information in the provided documents. "
            "Please consult a qualified legal professional for this question.' "
            
            "You provide informational guidance only, not legal advice. "
            "Always recommend consulting a qualified legal professional "
            "for binding compliance decisions. "
            
            "Structure your answer as follows: "
            "1. A direct answer in 2-3 sentences. "
            "2. A detailed explanation if needed. "
            "3. Sources in this format: [Document - Article/Section - Page]. "
            
            "Before answering, identify the most relevant passages from the context. "
            "Then check if your answer is fully supported by those passages. "
            "If you find any inconsistency, revise your answer before responding."
            "Provide open, nuanced responses and avoid definitive legal conclusions."
        ),
        input=f"Context:\n{context}\n\nQuestion:\n{user_question}"
    )

    return response.output_text 