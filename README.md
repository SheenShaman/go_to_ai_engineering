# Проект: AI Knowledge Agent

### Сделаем агента, который работает с базой знаний.

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
