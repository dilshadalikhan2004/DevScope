"""
DevScope - Time-Series & Trend Analysis Engine
Calculates Compound Annual Growth Rates (CAGR) and multi-year adoption momentum
for programming languages, databases, cloud providers, and AI tools across 2021-2024.
Normalizes survey mention counts per 1,000 respondents to control for sample size variance.
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from etl.logger import get_logger

logger = get_logger(__name__)

def calculate_multi_year_cagr() -> pd.DataFrame:
    """Calculates normalized 4-year CAGR (2021 to 2024) for programming languages."""
    logger.info("Calculating multi-year technology CAGR rates (2021-2024)...")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    # Get total respondent count by year for normalization
    resp_counts = pd.read_sql_query("SELECT survey_year, COUNT(*) as total_resp FROM respondents GROUP BY survey_year", engine)
    total_2021 = float(resp_counts[resp_counts["survey_year"] == 2021]["total_resp"].values[0])
    total_2024 = float(resp_counts[resp_counts["survey_year"] == 2024]["total_resp"].values[0])
    
    query = """
    SELECT 
        language_name,
        SUM(CASE WHEN survey_year = 2021 THEN 1 ELSE 0 END) AS raw_count_2021,
        SUM(CASE WHEN survey_year = 2024 THEN 1 ELSE 0 END) AS raw_count_2024
    FROM respondent_languages
    GROUP BY language_name
    """
    
    df = pd.read_sql_query(query, engine)
    df = df[(df["raw_count_2021"] >= 50) & (df["raw_count_2024"] >= 50)].copy()
    
    # Normalize per 1,000 respondents
    df["count_2021"] = (df["raw_count_2021"] / total_2021) * 1000.0
    df["count_2024"] = (df["raw_count_2024"] / total_2024) * 1000.0
    
    # Calculate normalized CAGR
    df["total_growth_pct"] = ((df["count_2024"] - df["count_2021"]) / df["count_2021"]) * 100.0
    df["cagr_pct"] = (np.power((df["count_2024"] / df["count_2021"]), (1.0 / 3.0)) - 1.0) * 100.0
    
    df["momentum_status"] = np.where(df["cagr_pct"] > 5.0, "Accelerating Growth",
                             np.where(df["cagr_pct"] >= -2.0, "Stable", "Declining"))
                             
    df = df.sort_values(by="cagr_pct", ascending=False).reset_index(drop=True)
    logger.info(f"Trend Analysis complete ({len(df)} technologies categorized by growth momentum).")
    return df

if __name__ == "__main__":
    trends = calculate_multi_year_cagr()
    print(trends)
