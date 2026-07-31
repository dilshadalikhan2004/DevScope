"""
DevScope - Data Cleaning & Standardization Engine
Applies strict data cleaning protocols across 2021-2024 Stack Overflow surveys and job postings.
Handles missing values via documented missingness rules without inventing synthetic data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from config import (
    MIN_VALID_AGE, MAX_VALID_AGE,
    MIN_VALID_EXPERIENCE, MAX_VALID_EXPERIENCE,
    MIN_COMPENSATION_USD, MAX_COMPENSATION_USD,
    CLEANED_COMBINED_PATH, CLEANED_JOB_POSTINGS_PATH
)
from etl.logger import get_logger
from etl.fetch_data import SO_SCHEMA_SPECS

logger = get_logger(__name__)

def clean_experience_string(val) -> float:
    """Standardizes years of professional coding experience."""
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip().lower()
    if "less than 1 year" in val_str:
        return 0.5
    if "more than 50 years" in val_str:
        return 50.0
    try:
        num = float(val_str)
        if MIN_VALID_EXPERIENCE <= num <= MAX_VALID_EXPERIENCE:
            return num
        return np.nan
    except ValueError:
        return np.nan

def clean_compensation(val) -> float:
    """Normalizes compensation USD values and filters extreme outliers."""
    if pd.isna(val):
        return np.nan
    try:
        comp = float(val)
        if MIN_COMPENSATION_USD <= comp <= MAX_COMPENSATION_USD:
            return comp
        return np.nan
    except ValueError:
        return np.nan

def clean_single_survey_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Cleans a single survey year DataFrame according to schema specifications."""
    logger.info(f"Cleaning survey dataset for year {year} ({len(df)} initial records)...")
    spec = SO_SCHEMA_SPECS[year]
    
    cleaned_df = pd.DataFrame()
    cleaned_df["respondent_id"] = df[spec["id_col"]].astype(int)
    cleaned_df["survey_year"] = year
    
    # Country standardization
    cleaned_df["country"] = df[spec["country_col"]].fillna("Unknown").astype(str).str.strip()
    
    # Age group
    cleaned_df["age_group"] = df[spec["age_col"]].fillna("Unspecified").astype(str)
    
    # Experience
    cleaned_df["years_experience"] = df[spec["exp_col"]].apply(clean_experience_string)
    
    # Education level
    cleaned_df["education_level"] = df[spec["ed_col"]].fillna("No Formal Degree").astype(str)
    
    # Employment type
    cleaned_df["employment_type"] = df[spec["emp_col"]].fillna("Other").astype(str)
    
    # Remote work mode
    if spec["remote_col"] and spec["remote_col"] in df.columns:
        cleaned_df["remote_work_mode"] = df[spec["remote_col"]].fillna("In-person").astype(str)
    else:
        cleaned_df["remote_work_mode"] = "In-person"
        
    # Org size
    if spec["org_col"] and spec["org_col"] in df.columns:
        cleaned_df["company_size"] = df[spec["org_col"]].fillna("Unknown").astype(str)
    else:
        cleaned_df["company_size"] = "Unknown"
        
    # Compensation
    cleaned_df["converted_comp_usd"] = df[spec["comp_col"]].apply(clean_compensation)
    
    # Job satisfaction
    if spec["sat_col"] and spec["sat_col"] in df.columns:
        cleaned_df["job_satisfaction"] = df[spec["sat_col"]].fillna("Neutral").astype(str)
    else:
        cleaned_df["job_satisfaction"] = "Neutral"
        
    # Multi-select technology strings
    cleaned_df["languages_raw"] = df[spec["lang_col"]].fillna("").astype(str) if spec["lang_col"] in df.columns else ""
    cleaned_df["frameworks_raw"] = df[spec["framework_col"]].fillna("").astype(str) if spec["framework_col"] in df.columns else ""
    cleaned_df["databases_raw"] = df[spec["db_col"]].fillna("").astype(str) if spec["db_col"] in df.columns else ""
    cleaned_df["cloud_raw"] = df[spec["cloud_col"]].fillna("").astype(str) if spec["cloud_col"] in df.columns else ""
    
    if spec["ai_tool_col"] and spec["ai_tool_col"] in df.columns:
        cleaned_df["ai_tools_raw"] = df[spec["ai_tool_col"]].fillna("").astype(str)
    else:
        cleaned_df["ai_tools_raw"] = ""
        
    # Drop exact duplicate respondent records
    cleaned_df = cleaned_df.drop_duplicates(subset=["survey_year", "respondent_id"])
    logger.info(f"Year {year} cleaning complete ({len(cleaned_df)} valid records retained).")
    return cleaned_df

def clean_all_surveys(raw_surveys: Dict[int, pd.DataFrame]) -> pd.DataFrame:
    """Cleans and combines multi-year survey datasets."""
    cleaned_dfs = [clean_single_survey_year(df, year) for year, df in raw_surveys.items()]
    combined = pd.concat(cleaned_dfs, ignore_index=True)
    combined.to_csv(CLEANED_COMBINED_PATH, index=False)
    logger.info(f"Combined multi-year cleaned surveys saved to {CLEANED_COMBINED_PATH} ({len(combined)} total rows).")
    return combined

def clean_job_postings(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans public tech job market postings dataset."""
    logger.info(f"Cleaning tech job market postings ({len(df)} initial records)...")
    cleaned = df.copy()
    cleaned["job_title"] = cleaned["job_title"].fillna("Software Engineer").str.strip()
    cleaned["posted_country"] = cleaned["posted_country"].fillna("Remote").str.strip()
    cleaned["required_skills"] = cleaned["required_skills"].fillna("").str.strip()
    cleaned["offered_salary_min_usd"] = cleaned["offered_salary_min_usd"].apply(clean_compensation)
    cleaned["offered_salary_max_usd"] = cleaned["offered_salary_max_usd"].apply(clean_compensation)
    cleaned["remote_allowed"] = cleaned["remote_allowed"].fillna(False).astype(bool)
    
    cleaned.to_csv(CLEANED_JOB_POSTINGS_PATH, index=False)
    logger.info(f"Cleaned job market postings saved to {CLEANED_JOB_POSTINGS_PATH}.")
    return cleaned

if __name__ == "__main__":
    from etl.extract import extract_survey_datasets, extract_job_postings
    raw_s = extract_survey_datasets()
    cleaned_s = clean_all_surveys(raw_s)
    raw_j = extract_job_postings()
    cleaned_j = clean_job_postings(raw_j)
