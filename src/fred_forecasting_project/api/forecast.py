from fastapi import APIRouter, Request

from fred_forecasting_project.core.rate_limiter import limiter
from fred_forecasting_project.services.forecast_service import get_unemployment_forecast

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)


@router.get("/unemployment")
@limiter.limit("30/minute")
async def unemployment_forecast(request: Request):
    return get_unemployment_forecast()