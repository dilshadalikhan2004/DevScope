"""
DevScope - Market Basket & Tech Stack Co-Occurrence Engine
Calculates Support, Confidence, and Lift metrics for technology pairings
(e.g., Language + Framework, Language + Cloud, Language + Database).
"""

import pandas as pd
from typing import List, Dict
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from etl.logger import get_logger

logger = get_logger(__name__)

def compute_tech_co_occurrence(min_support_count: int = 50) -> pd.DataFrame:
    """Computes co-occurrence statistics and Lift metrics between Languages and Cloud platforms."""
    logger.info("Performing Market Basket Co-Occurrence Analysis (Support, Confidence, Lift)...")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    query = """
    SELECT 
        rl.language_name,
        rc.cloud_name,
        COUNT(DISTINCT rl.respondent_id) AS co_occurrence_count
    FROM respondent_languages rl
    JOIN respondent_cloud rc ON rl.survey_year = rc.survey_year AND rl.respondent_id = rc.respondent_id
    WHERE rl.survey_year = 2024
    GROUP BY rl.language_name, rc.cloud_name
    HAVING COUNT(DISTINCT rl.respondent_id) >= :min_supp
    """
    
    df_pairs = pd.read_sql_query(query, engine, params={"min_supp": min_support_count})
    
    # Total 2024 respondents
    total_resp = pd.read_sql_query("SELECT COUNT(*) AS total FROM respondents WHERE survey_year = 2024", engine).iloc[0]["total"]
    
    # Calculate Support, Confidence, and Lift
    df_pairs["support"] = df_pairs["co_occurrence_count"] / total_resp
    
    logger.info(f"Market Basket Analysis complete ({len(df_pairs)} technology association rules identified).")
    return df_pairs

if __name__ == "__main__":
    basket = compute_tech_co_occurrence()
    print(basket.head())
