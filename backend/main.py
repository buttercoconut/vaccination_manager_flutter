from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as vaccination_router

app = FastAPI(title="Vaccination Manager API")

# CORS 설정 (필요 시 도메인 지정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(vaccination_router, prefix="/api/vaccinations", tags=["vaccinations"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
