from fastapi import FastAPI

from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.app_env
    }
