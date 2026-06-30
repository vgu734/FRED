from sqlalchemy.orm import sessionmaker
from fred_forecasting_project.database.engine import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)