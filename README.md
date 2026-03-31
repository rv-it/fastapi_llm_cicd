# FastAPI LLM Log Analyzer

## Overview

This project is a DevOps-oriented application that analyzes system logs using a Large Language Model (LLM) and sends a structured HTML report via email.  
It is designed to apply and consolidate concepts learned during the Cisco DevNet certification (API, CI/CD, Docker, automation).

**Technologies**:
- API development (FastAPI)
- CI/CD pipelines
- Docker & containerization
- Log processing (Linux / journalctl)
- LLM integration in real-world workflows

---

## Architecture

**ai/** → LLM log analysis logic  
**mail/** → Email sending logic  
**client/** → Log retrieval + API calls    
**client/docker_host/** → script to deploy container    
**tests/** → Unit tests (pytest)    
**main.py** → FastAPI entrypoint    
**Dockerfile** → Container image    
**.github/** → CI/CD pipeline    


---

## Workflow

1. Retrieve logs from `journalctl`  
2. Filter and aggregate logs  
3. Send logs to `/analyzer` endpoint  
4. LLM generates an HTML report  
5. Send report via `/mail` endpoint  

---

## Environment Variables

### API (container)

```bash
api_key=your_llm_api_key   
app_pwd_user=your_email_app_password 
```

### Client

```bash
api_hots_ip=your_docker_host  
model=gemini/gemini-2.5-flash  
smtp_srv=smtp.gmail.com   
port=587   
sender=your_email@gmail.com    
receiver=receiver@email.com   
```

---

## Deployment (CI/CD)

The Docker image is automatically built and pushed to **GitHub Container Registry (GHCR)** via GitHub Actions.

### Pipeline

On each push to `main`:

- run tests (`pytest`)  
- build Docker image (multi-architecture: amd64 + arm64)  
- push image to GHCR  

**Image**:

ghcr.io/<your-username>/fastapi-llm:latest



---

## Run the Application

Deployment is handled via the provided script:

```bash
bash client/docker_host/retrieved_container.sh
```

**This script will**:

- pull the latest image from GHCR
- stop and remove existing container
- run a new container with environment variable

## Run the Client
```bash
python -m client.api_call
```
**This will**:

- retrieve logs
- call the API
- send the email report

## Notes

This project is for learning purposes and not production-ready.

- No authentication  
- No rate limiting 
- Basic error handling 
