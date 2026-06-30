from fastapi import APIRouter, BackgroundTasks, Request

from fred_forecasting_project.core.rate_limiter import limiter
from fred_forecasting_project.services.job_service import run_fred_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/run-fred")
@limiter.limit("10/minute")
def run_fred_manual(request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_fred_job, source="manual")

    return {
        "status": "started",
        "message": "FRED job is running in background"
    }