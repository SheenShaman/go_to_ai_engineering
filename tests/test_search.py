from app.rag.embeddings import search_chunks

simple_question = "Какой индекс по умолчанию в Postgresql?"
norm_question = "Какие есть индексы?"

results = search_chunks(
    question=simple_question,
    top_k=2,
)

for result in results:
    print(f"\nДокумент: {result.filename}")
    print(f"Чанк: {result.chunk_index}")
    print(f"Distance: {result.distance:.4f}")
    print(result.content)
