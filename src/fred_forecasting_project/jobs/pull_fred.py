import logging
import os
import pandas as pd
import numpy as np

from fredapi import Fred

logger = logging.getLogger(__name__)

SERIES = {
    "unemployment_rate": "UNRATE",
    "labor_force_participation_rate": "CIVPART",
    "nonfarm_payroll_employment": "PAYEMS",
    "consumer_price_index": "CPIAUCSL",
    "core_consumer_price_index": "CPILFESL",
    "personal_consumption_expenditures_price_index": "PCEPI",
    "federal_funds_rate": "FEDFUNDS",
    "industrial_production_index": "INDPRO",
    "housing_starts": "HOUST",
    "gdp": "GDPC1"
}

def get_fred_client():
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

    df = pd.concat(series_list, axis=1)

    # Ensure datetime index
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # GDP: forward fill
    gdp_growth_q = np.log(df['gdp'].dropna()).diff()
    df['gdp_growth'] = gdp_growth_q.reindex(df.index, method='ffill')

    # Diff labor force participation rate
    df["labor_force_participation_rate_change"] = df["labor_force_participation_rate"].diff()

    # Keep only 1959-01-01 onward
    df = df.loc[df.index >= "1959-01-01"]

    # Log transforms
    df["nonfarm_payroll_employment_growth"] = np.log(df["nonfarm_payroll_employment"]).diff()
    df["cpi_growth"] = np.log(df["consumer_price_index"]).diff()
    df["core_consumer_price_index_growth"] = np.log(df["core_consumer_price_index"]).diff()
    df["personal_consumption_expenditures_price_index_growth"] = np.log(df["personal_consumption_expenditures_price_index"]).diff()
    df["industrial_production_index_growth"] = np.log(df["industrial_production_index"]).diff()

    # Log columns missing >1% of data, excluding gdp which is already transformed
    na_ratio = df.isna().mean().sort_values(ascending=False).drop(labels=["gdp"], errors="ignore")
    threshold = 0.01
    high_na = na_ratio[na_ratio > threshold]

    if not high_na.empty:
        logger.warning(
            "Columns with more than %.1f%% missing values:\n%s",
            threshold * 100,
            high_na.to_string(),
        )

    return df