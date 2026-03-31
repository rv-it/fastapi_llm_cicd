#!/bin/bash
docker pull ghcr.io/rv-it/fastapi-llm:latest
docker stop fastapi_llm || true   # || continu même si echec (ex: conteneur n'existe pas)
docker rm fastapi_llm || true
docker run -d --name fastapi_llm --env-file .env -p 8000:8000 ghcr.io/rv-it/fastapi-llm:latest
