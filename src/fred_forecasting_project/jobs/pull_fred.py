from fredapi import Fred
from dotenv import load_dotenv
import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)

SERIES = {
    "unemployment_rate": "UNRATE",
    "labor_force_participation_rate": "CIVPART",
    "consumer_price_index": "CPIAUCSL",
    "core_consumer_price_index": "CPILFESL",
    "personal_consumption_expenditures_price_index": "PCEPI",
    "federal_funds_rate": "FEDFUNDS",
    "industrial_production_index": "INDPRO",
    "housing_starts": "HOUST",
    "gdp": "GDPC1"
}

def get_fred_client():
    load_dotenv()

    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise ValueError("FRED_API_KEY is not set")

    return Fred(api_key=api_key)


def pull_fred():
    fred = get_fred_client()
    series_list = []

    for name, code in SERIES.items():
        s = fred.get_series(code)
        series_list.append(s.rename(name))

    raw_df = pd.concat(series_list, axis=1)

    # later: cleaning + postgres insert
    logger.info("FRED job ran")
    logger.info("\n%s", raw_df.tail(10))
    return raw_df