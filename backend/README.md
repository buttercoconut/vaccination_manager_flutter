# README.md
# Vaccination Manager Backend

This repository contains the FastAPI backend for the Vaccination Manager application.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn backend.main:app --reload
```

## Docker

```bash
docker build -t vaccination-backend .
docker run -p 8000:8000 vaccination-backend
```
