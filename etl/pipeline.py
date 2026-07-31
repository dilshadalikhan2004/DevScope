"""
DevScope - Master ETL Orchestrator
Executes the end-to-end Extract, Clean, Transform, and Load pipeline
across 2021-2024 Stack Overflow survey datasets and Tech Job Market Postings.
"""

import time
from etl.logger import get_logger
from etl.fetch_data import ensure_raw_datasets_exist
from etl.extract import extract_survey_datasets, extract_job_postings
from etl.clean import clean_all_surveys, clean_job_postings
from etl.transform import transform_survey_features, compute_executive_kpis
from etl.load import load_data_to_database

logger = get_logger(__name__)

def run_pipeline():
    """Runs full ETL pipeline lifecycle."""
    start_time = time.time()
    logger.info("==================================================")
    logger.info("Starting DevScope Master ETL Pipeline Lifecycle...")
    logger.info("==================================================")
    
    # 1. Data Availability Verification & Fetch
    ensure_raw_datasets_exist()
    
    # 2. Extract Phase
    raw_surveys = extract_survey_datasets()
    raw_jobs = extract_job_postings()
    
    # 3. Clean Phase
    cleaned_surveys = clean_all_surveys(raw_surveys)
    cleaned_jobs = clean_job_postings(raw_jobs)
    
    # 4. Transform & Feature Engineering Phase
    transformed_surveys = transform_survey_features(cleaned_surveys)
    kpis = compute_executive_kpis(transformed_surveys)
    
    # 5. Database Load Phase
    load_data_to_database()
    
    elapsed = round(time.time() - start_time, 2)
    logger.info("==================================================")
    logger.info(f"DevScope Master ETL Pipeline completed in {elapsed}s.")
    logger.info(f"Summary: {len(transformed_surveys)} survey records & {len(cleaned_jobs)} job postings ingested.")
    logger.info("==================================================")

if __name__ == "__main__":
    run_pipeline()
