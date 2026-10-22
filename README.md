# Проект: AI Knowledge Agent

### Сделаем агента, который работает с базой знаний небольшой компании.

Пользователь сможет:

- задавать вопросы по внутренней документации;
- искать информацию через RAG;
- получать данные из БД через tools;
- создавать/изменять записи;
- работать с историей диалога;
- использовать memory;
- объяснять, откуда взял информацию;
- выполнять несколько действий последовательно.

```
Python
│
├── LLM API
│
├── Prompting
│
├── Structured Output
│
├── Tool / Function Calling
│
├── Agent Loop
│
├── RAG
│ ├── Chunking
│ ├── Embeddings
│ ├── Vector Search
│ └── Vector DB
│
├── PostgreSQL
│
├── Memory
│
├── API / FastAPI
│
├── Evaluation
│
├── Logging / Observability
│
└── Docker
```

## План проекта

### Этап 1 — LLM

- подключаем модель;
- system/user messages;
- structured output;
- streaming.

### Этап 2 — Tools

- пишем обычные Python-функции;
- описываем их schema;
- подключаем function calling;
- делаем первый agent loop.

### Этап 3 — RAG

- документы;
- chunking;
- embeddings;
- cosine similarity;
- затем PostgreSQL + pgvector;
- metadata filtering.

### Этап 4 — полноценный Agent

```                
                ┌── get_customer()
                │
User → LLM ─────┼── search_knowledge()
                │
                ├── get_orders()
                │
                └── create_ticket()
                       ↓
                    Tool result
                       ↓
                       LLM
                       ↓
                    Answer
```

### Этап 5 — Memory

- conversation history;
- summary;
- long-term user memory;
- working state.

### Этап 6 — Production-ish

- FastAPI;
- Docker;
- PostgreSQL;
- конфигурация;
- retries/timeouts;
- permissions;
- logging.

### Этап 7 — Evaluation

Будем проверять не только «работает ли», но и:

1. Какие документы нашёл RAG?
2. Правильные ли chunks?
3. Правильно ли выбрал tool?
4. Правильные ли аргументы?
5. Правильный ли финальный ответ?
6. Сколько стоил запрос?
7. Сколько занял?

