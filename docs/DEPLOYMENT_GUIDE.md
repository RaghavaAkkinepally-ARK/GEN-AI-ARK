# Deployment Guide

## Local containers

```powershell
docker compose up --build
```

The current Compose file provides MongoDB and API scaffolding. The frontend container
is not yet linked to built React assets and must be built and served through a
frontend production stage before this claim is complete.

## AWS

AWS deployment is not verified. Create an AWS account, IAM deployment identity,
ECR repositories and ECS infrastructure only after secrets and cost controls are approved.
Store credentials only in GitHub Actions secrets or AWS Secrets Manager.

## External setup required

- MongoDB URI and database
- ChromaDB persistent storage
- Provider API credentials
- Weather service credentials
- AWS account and Terraform state backend
- Domain, TLS certificate and DNS

