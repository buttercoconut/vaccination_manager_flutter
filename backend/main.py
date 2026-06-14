# main.py
from fastapi import FastAPI
from . import routes, database, models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Vaccination Manager API")

origins = ["*"]  # In production restrict origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)
