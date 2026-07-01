import logging
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from .helpers.upsert_fred import upsert_fred
from fred_forecasting_project.jobs.pull_fred import pull_fred
from fred_forecasting_project.database.session import SessionLocal
from fred_forecasting_project.models.job_runs import JobRun

logger = logging.getLogger(__name__)
def _build_idempotency_key(source: str) -> str:
    now = datetime.now(timezone.utc)

    if source == "manual":
        time_part = now.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        # coarse-grained: day resolution
        time_part = now.strftime("%Y-%m-%d")

    return f"fred_pull:{source}:{time_part}"

"""
source: 'manual' | 'cron'
"""
def run_fred_job(source: str = "manual"):
    session = SessionLocal()
    idempotency_key = _build_idempotency_key(source)

    # Check for existing run
    existing = (
        session.query(JobRun)
        .filter(JobRun.idempotency_key == idempotency_key)
        .first()
    )

    if existing:
        if existing.status == "success":
            logger.info("Skipping job (already completed) idempotency_key=%s", idempotency_key)
            return {
                "status": "skipped",
                "reason": "already_completed",
                "idempotency_key": idempotency_key,
            }

        if existing.status == "running":
            logger.info("Job already running idempotency_key=%s", idempotency_key)
            return {
                "status": "skipped",
                "reason": "already_running",
                "idempotency_key": idempotency_key,
            }

    # Create run record
    job = JobRun(
        job_name="fred_pull",
        source=source,
        idempotency_key=idempotency_key,
        status="running",
        started_at=datetime.now(timezone.utc),
    )

    try:
        session.add(job)
        session.commit()
        session.refresh(job)

    except IntegrityError:
        session.rollback()
        logger.info("Duplicate run blocked by DB constraint idempotency_key=%s", idempotency_key)
        return {
            "status": "skipped",
            "reason": "duplicate_key",
            "idempotency_key": idempotency_key,
        }

    # Run the job
    try:
        logger.info("FRED job started | source=%s | time=%s",
                    source,
                    datetime.now(timezone.utc))

        df = pull_fred()
        upsert_fred(session, df)

        job.status = "success"
        job.finished_at = datetime.now(timezone.utc)
        session.commit()

        logger.info(
            "FRED job finished | source=%s | rows=%s cols=%s",
            source,
            df.shape[0],
            df.shape[1],
        )

        return {
            "status": "success",
            "source": source,
            "rows": df.shape[0],
            "cols": df.shape[1],
            "idempotency_key": idempotency_key,
        }
    
    except Exception as e:
        session.rollback()

        job.status = "failed"
        job.finished_at = datetime.now(timezone.utc)
        job.error_message = str(e)

        session.add(job)
        session.commit()

        logger.exception("FRED job failed idempotency_key=%s", idempotency_key)

        raise

    finally:
        session.close()