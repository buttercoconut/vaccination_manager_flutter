"""FastAPI application entry point."""

from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Vaccination Manager API")

app.include_router(router)

# For future: include authentication, database, etc.
