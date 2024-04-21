from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("thenlper/gte-large")

def get_embedding(text: str) -> list[float]:
  if not text:
    print("No text provided to embed")
    return []

  embedding = embedding_model.encode(text)
  return embedding.tolist()