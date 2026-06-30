from contextlib import asynccontextmanager

from fred_forecasting_project.database.base import Base
from fred_forecasting_project.database.engine import engine
from fred_forecasting_project.infrastructure.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app):
    # startup
    Base.metadata.create_all(bind=engine)
    start_scheduler()

    yield

    # shutdown
    # e.g. close connections, flush caches, etc.
    stop_scheduler()