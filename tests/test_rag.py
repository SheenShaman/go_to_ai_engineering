from app.rag.embeddings import search_chunks
from app.rag.generation import generation_answer


def test_llm_answer(question: str):
    chunks = search_chunks(question=question, top_k=3)

    llm_answer = generation_answer(
        question=question,
        chunks=chunks,
    )

    result = ["\nОтвет:", llm_answer.answer, "\nИсточники:"]

    for source in llm_answer.sources:
        result.append(f"""
        - {source["filename"]},
        чанк {source["chunk_index"]}
        """)
    return result


# print(test_llm_answer("Какой индекс по умолчанию в PostgreSQL?"))
# print(test_llm_answer("Для чего используется GIN?"))
print(test_llm_answer("Кто создал PostgreSQL?"))
