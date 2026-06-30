from apscheduler.schedulers.background import BackgroundScheduler
import logging

from fred_forecasting_project.services.job_service import run_fred_job

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def scheduled_job():
    try:
        run_fred_job(source="cron")
    except Exception:
        logger.exception("FRED cron job failed")


def start_scheduler():
    scheduler.add_job(
        scheduled_job,
        trigger="cron",
        day=10,
        hour=0,
        minute=0,
        id="fred_monthly_job",
        replace_existing=True,
    )
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()