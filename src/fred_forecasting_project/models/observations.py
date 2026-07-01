from sqlalchemy import Column, Float, Date
from fred_forecasting_project.database.base import Base

class Observation(Base):
    __tablename__ = "observations"

    date = Column(Date, primary_key=True)

    unemployment_rate = Column(Float)
    labor_force_participation_rate = Column(Float)
    nonfarm_payroll_employment = Column(Float)
    consumer_price_index = Column(Float)
    core_consumer_price_index = Column(Float)
    personal_consumption_expenditures_price_index = Column(Float)
    federal_funds_rate = Column(Float)
    industrial_production_index = Column(Float)
    housing_starts = Column(Float)
    gdp = Column(Float)

    gdp_growth = Column(Float)
    labor_force_participation_rate_change = Column(Float)
    nonfarm_payroll_employment_growth = Column(Float)
    cpi_growth = Column(Float)
    core_consumer_price_index_growth = Column(Float)
    personal_consumption_expenditures_price_index_growth = Column(Float)
    industrial_production_index_growth = Column(Float)