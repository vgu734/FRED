from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone

from fred_forecasting_project.database.base import Base


class JobRun(Base):
    __tablename__ = "job_runs"

    id = Column(Integer, primary_key=True, index=True)

    job_name = Column(String, index=True, nullable=False)   # e.g. "fred_pull"
    source = Column(String, nullable=False)                 # "manual" | "cron"

    idempotency_key = Column(String, unique=True, index=True, nullable=False)

    status = Column(String, index=True, nullable=False)     # "running" | "success" | "failed"

    started_at = Column(DateTime(timezone=True), nullable=False)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    error_message = Column(Text, nullable=True)