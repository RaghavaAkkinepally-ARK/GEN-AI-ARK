# Architecture Decision Records

## ADR-001: Provider-agnostic API

**Status:** Accepted

Use a shared request/response contract and provider-specific adapters. This keeps
token accounting, tracing and routing independent of a vendor SDK.

## ADR-002: QLoRA adapter storage

**Status:** Accepted

Store only LoRA adapter artifacts, never merge them into base model weights in the
default workflow. The base model and license must be recorded explicitly.

## ADR-003: Retrieval evidence

**Status:** Accepted

RAG answers must cite retrieved chunks and must decline unsupported claims.
Retrieved evidence is separate from model-generated recommendations.

