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
def health(request: Request):
    app = request.app
    model = getattr(app.state, "model", None)
    model_ok = model is not None

    return {
        # "status": "ok" if model_ok else "degraded", TODO: implement once ML model pipeline exists
        "database": "connected" if app.state.db_ready else "disconnected",
        "model_loaded": model_ok
    }