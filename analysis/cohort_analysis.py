"""
DevScope - Cohort Analysis Engine
Tracks developer experience cohorts (0-2 yrs, 3-5 yrs, 6-10 yrs, 11+ yrs) and education levels
across 2021-2024 to evaluate salary progression, remote work shifts, and skill retention.
"""

import pandas as pd
from typing import Dict
from config import CLEANED_COMBINED_PATH
from etl.logger import get_logger
from etl.transform import transform_survey_features

logger = get_logger(__name__)

def analyze_experience_cohorts() -> pd.DataFrame:
    """Computes median salary progression by experience cohort across survey years."""
    logger.info("Performing multi-year experience cohort analysis...")
    df = pd.read_csv(CLEANED_COMBINED_PATH)
    df = transform_survey_features(df)
    
    cohort_summary = (
        df.groupby(["survey_year", "experience_bucket"])
        .agg(
            developer_count=("respondent_id", "count"),
            median_salary_usd=("converted_comp_usd", "median"),
            avg_skill_diversity=("skill_diversity_index", "mean"),
            ai_adoption_rate=("has_ai_adoption", lambda x: round(x.mean() * 100, 2))
        )
        .reset_index()
    )
    
    logger.info("Experience cohort analysis complete.")
    return cohort_summary

if __name__ == "__main__":
    cohorts = analyze_experience_cohorts()
    print(cohorts)
