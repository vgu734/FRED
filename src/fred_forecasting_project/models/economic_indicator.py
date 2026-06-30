from sqlalchemy import Column, Integer, Float, Date
from fred_forecasting_project.database.base import Base


class EconomicIndicator(Base):
    __tablename__ = "economic_indicators"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    value = Column(Float, nullable=False)