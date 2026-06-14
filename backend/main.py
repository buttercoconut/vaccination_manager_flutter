"""
FastAPI application entry point for Vaccination Manager backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router as api_router

app = FastAPI(title="Vaccination Manager API", version="0.1.0")

# Allow CORS for Flutter app (localhost:3000 or mobile)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Vaccination Manager API"}
