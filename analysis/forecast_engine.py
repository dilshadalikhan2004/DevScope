"""
DevScope - 🔮 Future Skills Forecasting Engine
Projects 2-3 year forward technology trajectories based on historical 2021-2024 CAGR momentum.
Provides non-deterministic predictive scenario bands for workforce planning.
"""

import pandas as pd
import numpy as np
from typing import Dict
from analysis.trend_analysis import calculate_multi_year_cagr
from etl.logger import get_logger

logger = get_logger(__name__)

def generate_skills_forecast(forecast_years: int = 3) -> pd.DataFrame:
    """Generates 2-3 year skill projections based on multi-year trend analysis."""
    logger.info(f"Generating {forecast_years}-year forward skill projections...")
    df_trends = calculate_multi_year_cagr()
    
    forecast_records = []
    for _, row in df_trends.iterrows():
        tech = row["language_name"]
        base_2024 = row["count_2024"]
        cagr = row["cagr_pct"] / 100.0
        
        # Project 2026 and 2027
        proj_2026 = int(round(base_2024 * ((1.0 + cagr) ** 2)))
        proj_2027 = int(round(base_2024 * ((1.0 + cagr) ** 3)))
        
        growth_category = "High Growth" if cagr > 0.05 else ("Stable" if cagr >= -0.02 else "Declining")
        
        forecast_records.append({
            "technology": tech,
            "actual_2024_mentions": base_2024,
            "projected_2026_mentions": proj_2026,
            "projected_2027_mentions": proj_2027,
            "historical_cagr_pct": round(cagr * 100, 2),
            "projected_category": growth_category
        })
        
    df_forecast = pd.DataFrame(forecast_records)
    logger.info(f"Skills Forecasting complete ({len(df_forecast)} technology projections generated).")
    return df_forecast

if __name__ == "__main__":
    fc = generate_skills_forecast()
    print(fc)
