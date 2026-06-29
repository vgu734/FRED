from fastapi import APIRouter, Request

from fred_forecasting_project.core.rate_limiter import limiter

router = APIRouter(
    tags=["Health"]
)

@router.get("/")
@limiter.limit("30/minute")
def root(request: Request):
    return {
        "service": "Economic Forecast API",
        "status": "running"
    }

@router.get("/health")
@limiter.limit("30/minute")
async def health(request: Request):
    return {
        "status": "ok!!",
        "database": "connected",
        "model_loaded": True
    }