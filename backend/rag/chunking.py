import tiktoken

def chunk_text(text : list, chunk_tokens : int = 450, overlap_tokens: int = 80) -> list:
    enc = tiktoken.get_encoding("cl100k_base")#Encodeur en token pour gpt4 "tokenizer"
    chunks = []
    for page in text:
        tokens = enc.encode(page["text"])
        start = 0
        while start < len(tokens):
            end = min(start + chunk_tokens, len(tokens))
            chunk = enc.decode(tokens[start:end])
            chunks.append({"text": chunk, "page": page["page"]})
            start = end - overlap_tokens
            if start < 0 or end == len(tokens):
                break

    return chunks