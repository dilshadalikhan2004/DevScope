"""
DevScope - Exploratory Data Analysis (EDA) Module
Generates statistical summaries, missingness logs, demographic distributions,
and geographic compensation profiles across 2021-2024 survey datasets.
"""

import pandas as pd
import numpy as np
from typing import Dict
from config import CLEANED_COMBINED_PATH
from etl.logger import get_logger

logger = get_logger(__name__)

def run_eda_summary() -> Dict:
    """Executes exploratory data analysis profiling."""
    logger.info("Executing Exploratory Data Analysis (EDA) profiling...")
    df = pd.read_csv(CLEANED_COMBINED_PATH)
    
    total_records = len(df)
    years = sorted(df["survey_year"].unique().tolist())
    
    # Missingness summary
    missingness = df.isnull().mean().to_dict()
    
    # Country distribution (2024)
    df_2024 = df[df["survey_year"] == 2024]
    top_countries = df_2024["country"].value_counts().head(10).to_dict()
    
    # Salary quantiles (2024)
    comp_series = df_2024["converted_comp_usd"].dropna()
    salary_quantiles = {
        "p25": float(comp_series.quantile(0.25)),
        "median": float(comp_series.median()),
        "p75": float(comp_series.quantile(0.75)),
        "mean": float(comp_series.mean()),
        "std": float(comp_series.std())
    }
    
    eda_results = {
        "total_records": total_records,
        "survey_years": years,
        "top_countries_2024": top_countries,
        "salary_quantiles_2024": salary_quantiles,
        "missingness_rates": {k: round(v * 100, 2) for k, v in missingness.items()}
    }
    
    logger.info(f"EDA Summary Complete: Analyzed {total_records} records across years {years}.")
    return eda_results

if __name__ == "__main__":
    results = run_eda_summary()
    print(results)
