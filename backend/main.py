"""
FastAPI backend for Vaccination Manager application.

This module sets up the FastAPI app, includes routers, and configures the database.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import routes, models
from .database import engine, SessionLocal

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vaccination Manager API")

# Allow CORS for Flutter app (localhost:3000 or mobile)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.user_router, prefix="/users", tags=["users"])
app.include_router(routes.vaccination_router, prefix="/vaccinations", tags=["vaccinations"])
app.include_router(routes.vaccine_router, prefix="/vaccines", tags=["vaccines"])

# Dependency for DB session
from fastapi import Depends

@app.middleware("http")
async def db_session_middleware(request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to Vaccination Manager API"}
