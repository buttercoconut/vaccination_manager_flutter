"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import routes, models
from .database import engine, SessionLocal

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vaccination Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.user_router, prefix="/users", tags=["users"])
app.include_router(routes.vaccination_router, prefix="/vaccinations", tags=["vaccinations"])
app.include_router(routes.vaccine_router, prefix="/vaccines", tags=["vaccines"])

@app.get("/")
async def root():
    return {"message": "Vaccination Manager API is running"}
