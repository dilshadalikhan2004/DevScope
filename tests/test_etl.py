"""
DevScope - ETL Extraction Unit Tests
"""

import pytest
from etl.extract import extract_survey_datasets, extract_job_postings

def test_extract_survey_datasets():
    surveys = extract_survey_datasets()
    assert len(surveys) == 4
    for year in [2021, 2022, 2023, 2024]:
        assert year in surveys
        assert not surveys[year].empty

def test_extract_job_postings():
    jobs = extract_job_postings()
    assert not jobs.empty
    assert "job_id" in jobs.columns
