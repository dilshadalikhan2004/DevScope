"""
DevScope - Database Loader Engine
Loads transformed datasets into PostgreSQL star schema or zero-config SQLite relational database.
Supports bulk inserting respondents, job postings, and exploded technology tables.
"""

import pandas as pd
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI, CLEANED_COMBINED_PATH, CLEANED_JOB_POSTINGS_PATH
from etl.logger import get_logger
from etl.transform import transform_survey_features, explode_multi_select_tags

logger = get_logger(__name__)

def load_data_to_database(db_uri: str = SQLALCHEMY_DATABASE_URI):
    """Loads cleaned survey data and job market postings into relational database tables."""
    logger.info(f"Connecting to database engine: {db_uri.split('@')[-1]}...")
    engine = create_engine(db_uri)
    
    df_surveys = pd.read_csv(CLEANED_COMBINED_PATH)
    df_transformed = transform_survey_features(df_surveys)
    
    # 1. Load Main Respondents Table
    logger.info(f"Loading {len(df_transformed)} rows into 'respondents' table...")
    df_transformed.to_sql("respondents", engine, if_exists="replace", index=False)
    
    # 2. Load Exploded Technology Tag Junction Tables
    logger.info("Exploding multi-select technology tags for relational indexing...")
    
    print("DEBUG: df_transformed languages_raw head:")
    print(df_transformed[["respondent_id", "survey_year", "languages_raw"]].head(20))
    print("DEBUG: df_transformed languages_raw top value counts:")
    print(df_transformed["languages_raw"].value_counts().head(20))

    df_langs = explode_multi_select_tags(df_transformed, "languages_raw", "language_name")
    logger.info(f"Loading {len(df_langs)} rows into 'respondent_languages'...")
    df_langs.to_sql("respondent_languages", engine, if_exists="replace", index=False)
    
    df_fw = explode_multi_select_tags(df_transformed, "frameworks_raw", "framework_name")
    logger.info(f"Loading {len(df_fw)} rows into 'respondent_frameworks'...")
    df_fw.to_sql("respondent_frameworks", engine, if_exists="replace", index=False)
    
    df_db = explode_multi_select_tags(df_transformed, "databases_raw", "database_name")
    logger.info(f"Loading {len(df_db)} rows into 'respondent_databases'...")
    df_db.to_sql("respondent_databases", engine, if_exists="replace", index=False)
    
    df_cloud = explode_multi_select_tags(df_transformed, "cloud_raw", "cloud_name")
    logger.info(f"Loading {len(df_cloud)} rows into 'respondent_cloud'...")
    df_cloud.to_sql("respondent_cloud", engine, if_exists="replace", index=False)
    
    df_ai = explode_multi_select_tags(df_transformed, "ai_tools_raw", "ai_tool_name")
    logger.info(f"Loading {len(df_ai)} rows into 'respondent_ai_tools'...")
    df_ai.to_sql("respondent_ai_tools", engine, if_exists="replace", index=False)
    
    # 3. Load Job Market Postings
    df_jobs = pd.read_csv(CLEANED_JOB_POSTINGS_PATH)
    logger.info(f"Loading {len(df_jobs)} rows into 'job_postings' table...")
    df_jobs.to_sql("job_postings", engine, if_exists="replace", index=False)
    
    logger.info("Database load completed successfully.")

if __name__ == "__main__":
    load_data_to_database()
