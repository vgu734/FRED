from contextlib import asynccontextmanager
from sqlalchemy import text

from fred_forecasting_project.database.base import Base
from fred_forecasting_project.database.engine import engine
from fred_forecasting_project.database.session import SessionLocal
from fred_forecasting_project.infrastructure.scheduler import start_scheduler, stop_scheduler

def check_db_session():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception:
        return False

@asynccontextmanager
async def lifespan(app):
    # startup
    Base.metadata.create_all(bind=engine)
    start_scheduler()

    # store shared state
    app.state.db_session_factory = SessionLocal
    app.state.db_ready = check_db_session()

    # model placeholder
    app.state.model = None
    app.state.model_loaded = False

    yield

    # shutdown
    # e.g. close connections, flush caches, etc.
    stop_scheduler()