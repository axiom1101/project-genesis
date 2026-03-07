from fastapi import FastAPI
from src.interface.api.routes import router as api_router

app = FastAPI(title="Project Genesis AI Core")

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "core": "online"}