from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from importlib.metadata import version

from fred_forecasting_project.api.forecast import router as forecast_router
from fred_forecasting_project.api.health import router as health_router
from fred_forecasting_project.api.jobs_api import router as jobs_router
from fred_forecasting_project.core.rate_limiter import limiter
from fred_forecasting_project.core.logging import setup_logging
from fred_forecasting_project.infrastructure.lifespan import lifespan

setup_logging()

app = FastAPI(
    title="Economic Forecast API",
    version=version("fred-forecasting-project"),
    lifespan=lifespan,
)

app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "https://yourdomain.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Content-Type", "Authorization"],
)
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests"}
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors()
        }
    )

app.include_router(forecast_router)
app.include_router(health_router)
app.include_router(jobs_router)