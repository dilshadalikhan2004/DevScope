"""
DevScope - Extraction & Schema Validation Engine
Reads multi-year raw CSV files, validates schemas, logs data shapes,
and prepares raw DataFrames for the cleaning pipeline.
"""

import pandas as pd
from typing import Dict
from config import RAW_SURVEY_PATHS, RAW_JOB_POSTINGS_PATH, SURVEY_YEARS
from etl.logger import get_logger
from etl.fetch_data import SO_SCHEMA_SPECS, ensure_raw_datasets_exist

logger = get_logger(__name__)

def extract_survey_datasets() -> Dict[int, pd.DataFrame]:
    """Extracts raw Stack Overflow survey datasets for all configured years."""
    ensure_raw_datasets_exist()
    extracted_surveys = {}
    
    for year in SURVEY_YEARS:
        path = RAW_SURVEY_PATHS[year]
        logger.info(f"Extracting raw survey data for year {year} from {path}...")
        df = pd.read_csv(path, low_memory=False)
        logger.info(f"Year {year} raw extraction complete. Shape: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        # Verify mandatory columns
        spec = SO_SCHEMA_SPECS[year]
        missing_cols = [col_val for col_key, col_val in spec.items() if col_val and col_val not in df.columns]
        if missing_cols:
            logger.warning(f"Year {year} missing expected schema columns: {missing_cols}")
            
        extracted_surveys[year] = df
        
    return extracted_surveys

def extract_job_postings() -> pd.DataFrame:
    """Extracts raw public tech job market postings dataset."""
    ensure_raw_datasets_exist()
    logger.info(f"Extracting job market postings from {RAW_JOB_POSTINGS_PATH}...")
    df = pd.read_csv(RAW_JOB_POSTINGS_PATH)
    logger.info(f"Job postings extraction complete. Shape: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df

if __name__ == "__main__":
    surveys = extract_survey_datasets()
    jobs = extract_job_postings()
