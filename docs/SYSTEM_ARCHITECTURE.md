# System Architecture

```text
React/Vite
    |
    v
FastAPI API Gateway
    |
    +-- Authentication
    +-- LLM Providers
    +-- Prompt Registry
    +-- Model Router
    |      +-- Prompting
    |      +-- RAG
    |      +-- QLoRA
    +-- Agricultural Tools
    +-- Evaluation
    +-- Observability
    +-- Ethics/Safety
    |
    +-- MongoDB
    +-- ChromaDB
```

All provider credentials stay in environment variables. The mock provider is the
safe default for local tests and must not be presented as an agricultural authority.

