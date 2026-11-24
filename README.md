# AgricultureGPT

AgricultureGPT is a modular, provider-agnostic agricultural advisory platform being
developed in phases for LLM engineering, RAG, QLoRA fine-tuning, security and
full-stack deployment.

## Repository status

This is an active implementation scaffold. External services and credentials are
not assumed. Generated model weights and API keys must never be committed.

## Quick start

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

API documentation is available at `http://localhost:8000/docs`.

## Planned structure

- `app/`: FastAPI application and modular services
- `frontend/`: React, Vite and TypeScript interface
- `experiments/`: reproducible CO1-CO5 experiments
- `scripts/`: data, evaluation and deployment utilities
- `notebooks/`: QLoRA training notebook
- `docs/`: architecture, governance and operating documentation
- `terraform/`: AWS infrastructure
- `tests/`: pytest and integration coverage

