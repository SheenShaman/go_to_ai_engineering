from sentence_transformers import SentenceTransformer
import hashlib
from pathlib import Path

import psycopg
from pgvector.psycopg import register_vector

from app.constants import DATABASE_URL, VECTORS_MODEL
from app.schemas import ChunksConfig
from psycopg import connect

from app.schemas import Chunk


model = SentenceTransformer(VECTORS_MODEL)


def embed_documents(chunks: list[str]) -> list[list[float]]:
    """
    Превращает текст в вектор

    Для E5 документы помечаются префиксом passage:
    """
    texts = [f"passage: {chunk}" for chunk in chunks]

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    return vectors.tolist()


def embed_query(question: str) -> list[float]:
    """
    Превращает вопрос в вектор

    Запросы помечаются префиксом query:
    """
    vector = model.encode(
        f"query: {question}",
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    return vector.tolist()


def split_into_chunks(config: ChunksConfig) -> list[str]:
    """
    Разбиваем текст на чанки с перекрытием. Вариант по символам.
    """
    if config.chunk_size <= 0:
        raise ValueError("chunk_size должен быть положительным")

    if not 0 <= config.overlap < config.chunk_size:
        raise ValueError("overlap должен быть >= 0 и меньше chunk_size")

    data = config.data.strip()
    chunks = []
    step = config.chunk_size - config.overlap

    for i in range(0, len(data), step):
        chunk = data[i : i + config.chunk_size].strip()

        if chunk:
            chunks.append(chunk)

        if i + config.chunk_size >= len(data):
            break

    return chunks


def ingest_document(path: Path, database_url: str = DATABASE_URL) -> int:
    """
    Добавление документов и их чанков в БД
    """
    # 1. Читаем документ
    text = path.read_text(encoding="utf-8")

    # 2. Считаем хэш содержимого
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    # 3. Разбиваем на фрагменты
    chunks = split_into_chunks(text)

    if not chunks:
        raise ValueError("Документ пустой")

    # 4. Вычисляем вектор для каждого фрагмента
    embeddings = embed_documents(chunks)

    # 5. Сохраняем документ и его фрагменты
    with psycopg.connect(database_url) as conn:
        register_vector(conn)

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (filename, content_hash)
                VALUES (%s, %s)
                ON CONFLICT (content_hash) DO NOTHING
                RETURNING id
                """,
                (path.name, content_hash),
            )

            row = cur.fetchone()

            if row is None:
                # Документ с таким содержимым уже есть
                cur.execute(
                    """
                    SELECT id FROM documents
                    WHERE content_hash = %s
                    """,
                    (content_hash,),
                )
                document_id = cur.fetchone()[0]
                return document_id

            document_id = row[0]

            # Индекс — порядковый номер фрагмента
            for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                cur.execute(
                    """
                    INSERT INTO chunks (
                        document_id,
                        chunk_index,
                        content,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (document_id, index, chunk, embedding),
                )

    return document_id


def search_chunks(
    question: str,
    database_url: str = DATABASE_URL,
    top_k: int = 5,
) -> list[Chunk]:
    """
    Возвращает top_k chunks под запрос
    """

    query_embeddings = embed_query(question)

    with connect(database_url) as conn:
        register_vector(conn)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.id,
                    d.filename,
                    c.chunk_index,
                    c.content,
                    c.embedding <=> %s::vector AS distance
                FROM chunks AS c
                JOIN documents AS d ON d.id = c.document_id
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s
                """,
                (query_embeddings, query_embeddings, top_k),
            )

            rows = cur.fetchall()

    return [
        Chunk(
            chunk_id=row[0],
            filename=row[1],
            chunk_index=row[2],
            content=row[3],
            distance=float(row[4]),
        )
        for row in rows
    ]