"""
DevScope - Developer Behavioral Segmentation Engine
Clusters developer survey respondents into 4 key strategic talent personas:
1. AI Innovators
2. Cloud-Native Engineers
3. Full-Stack Generalists
4. Legacy Enterprise Specialists
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from etl.logger import get_logger

logger = get_logger(__name__)

def segment_developer_personas() -> pd.DataFrame:
    """Classifies developers into 4 strategic behavioral personas."""
    logger.info("Executing Developer Behavioral Segmentation...")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    query = """
    SELECT 
        respondent_id,
        survey_year,
        country,
        years_experience,
        converted_comp_usd,
        skill_diversity_index,
        has_ai_adoption,
        languages_raw,
        cloud_raw
    FROM respondents
    WHERE survey_year = 2024
    """
    
    df = pd.read_sql_query(query, engine)
    
    def classify_persona(row) -> str:
        ai = row["has_ai_adoption"]
        cloud = str(row["cloud_raw"]).lower()
        div = row["skill_diversity_index"]
        
        if ai and ("aws" in cloud or "google cloud" in cloud or "azure" in cloud):
            return "AI & Cloud Innovators"
        elif "aws" in cloud or "google cloud" in cloud or "azure" in cloud:
            return "Cloud-Native Specialists"
        elif div >= 8:
            return "Full-Stack Generalists"
        else:
            return "Legacy Enterprise Specialists"
            
    df["developer_persona"] = df.apply(classify_persona, axis=1)
    
    persona_summary = (
        df.groupby("developer_persona")
        .agg(
            developer_count=("respondent_id", "count"),
            median_salary_usd=("converted_comp_usd", "median"),
            avg_experience=("years_experience", "mean"),
            avg_skill_diversity=("skill_diversity_index", "mean")
        )
        .reset_index()
    )
    
    logger.info("Developer Behavioral Segmentation complete.")
    return persona_summary

if __name__ == "__main__":
    personas = segment_developer_personas()
    print(personas)
