"""
DevScope - Developer Supply vs. Employer Demand Gap Analysis Engine
Quantifies skill deficits and surpluses by joining developer survey supply data
against employer job market posting demand.
"""

import pandas as pd
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from etl.logger import get_logger

logger = get_logger(__name__)

def analyze_supply_demand_gaps() -> pd.DataFrame:
    """Computes demand-to-supply ratios across key tech stack skills."""
    logger.info("Performing Developer Supply vs. Employer Demand Gap Analysis...")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    # 1. Fetch Developer Supply Count (2024 Survey)
    query_supply = """
    SELECT 'AWS' AS skill, COUNT(*) AS dev_supply FROM respondent_cloud WHERE survey_year = 2024 AND cloud_name = 'AWS'
    UNION ALL
    SELECT 'Python', COUNT(*) FROM respondent_languages WHERE survey_year = 2024 AND language_name = 'Python'
    UNION ALL
    SELECT 'Rust', COUNT(*) FROM respondent_languages WHERE survey_year = 2024 AND language_name = 'Rust'
    UNION ALL
    SELECT 'Kubernetes', COUNT(*) FROM respondent_cloud WHERE survey_year = 2024 AND cloud_name = 'Kubernetes'
    UNION ALL
    SELECT 'TypeScript', COUNT(*) FROM respondent_languages WHERE survey_year = 2024 AND language_name = 'TypeScript'
    """
    df_supply = pd.read_sql_query(query_supply, engine)
    
    # 2. Fetch Job Posting Demand Count
    query_demand = """
    SELECT 'AWS' AS skill, COUNT(*) AS job_demand FROM job_postings WHERE required_skills LIKE '%AWS%'
    UNION ALL
    SELECT 'Python', COUNT(*) FROM job_postings WHERE required_skills LIKE '%Python%'
    UNION ALL
    SELECT 'Rust', COUNT(*) FROM job_postings WHERE required_skills LIKE '%Rust%'
    UNION ALL
    SELECT 'Kubernetes', COUNT(*) FROM job_postings WHERE required_skills LIKE '%Kubernetes%'
    UNION ALL
    SELECT 'TypeScript', COUNT(*) FROM job_postings WHERE required_skills LIKE '%TypeScript%'
    """
    df_demand = pd.read_sql_query(query_demand, engine)
    
    # 3. Merge & Compute Gap Index
    df_merged = pd.merge(df_demand, df_supply, on="skill")
    df_merged["demand_to_supply_ratio"] = round(df_merged["job_demand"] / df_merged["dev_supply"], 3)
    df_merged["gap_severity"] = pd.qcut(df_merged["demand_to_supply_ratio"], q=3, labels=["Low Deficit", "Moderate Deficit", "High Deficit"])
    
    df_merged = df_merged.sort_values(by="demand_to_supply_ratio", ascending=False).reset_index(drop=True)
    logger.info("Supply vs Demand Gap Analysis complete.")
    return df_merged

if __name__ == "__main__":
    gaps = analyze_supply_demand_gaps()
    print(gaps)
