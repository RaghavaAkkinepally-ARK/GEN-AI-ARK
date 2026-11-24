# API Documentation

FastAPI documentation is generated at `/docs` and the OpenAPI schema at `/openapi.json`.

## Endpoints

- `GET /health`: service health
- `POST /llm/generate`: provider interface smoke call
- `POST /rag/query`: retrieval and citation response
- `POST /advisory/answer`: prompt and safety boundary

No endpoint is a source of verified live weather or soil data unless explicitly
connected to an approved external provider.
