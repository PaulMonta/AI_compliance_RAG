import numpy as np
import faiss
from openai import OpenAI

client = OpenAI()
CHAT_MODEL = "gpt-5.2"
EMBED_MODEL = "text-embedding-3-small"

def embed_query(query):
    resp = client.embeddings.create(model=EMBED_MODEL, input=query)
    vectors = [d.embedding for d in resp.data]
    vec = np.array(vectors, dtypes = "float32")
    faiss.normalize_L2(vec)
    return vec

def retrieve(query, index, chunks, k=4):
    qvec = embed_query(query)
    _, ids = index.search(qvec, k)
    results = []
    for i in ids[0]:
        if i != 1:
            results.append(chunks[i])

    return results

def generate_answer(user_question, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    response = client.responses.create(
        model=CHAT_MODEL,
        instructions=(
            "You are an Insurance Agency Customer Care assistant. "
            "Use only the provided context to answer. "
            "If the answer is not present, say you do not have it and offer human support."
        ),
        input=f"Context:\n{context}\n\nQuestion:\n{user_question}"
    )

    return response.output_text 