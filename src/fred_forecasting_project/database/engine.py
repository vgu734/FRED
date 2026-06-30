from sqlalchemy import create_engine
from fred_forecasting_project.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)