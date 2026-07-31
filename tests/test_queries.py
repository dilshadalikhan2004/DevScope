"""
DevScope - SQL Business Query Integration Tests
Executes representative queries from each consolidated SQL file to verify
syntax correctness and expected return types.
"""

import pytest
import pandas as pd
from sqlalchemy import create_engine, text
from config import SQLALCHEMY_DATABASE_URI


@pytest.fixture(scope="module")
def db_engine():
    return create_engine(SQLALCHEMY_DATABASE_URI)


def test_salary_country_query(db_engine):
    """Validates global salary benchmark query returns country-level rows."""
    query = """
        SELECT country, COUNT(*) AS total, AVG(converted_comp_usd) AS avg_salary
        FROM respondents
        WHERE survey_year = 2024 AND converted_comp_usd IS NOT NULL
        GROUP BY country
        HAVING COUNT(*) >= 10
        ORDER BY avg_salary DESC
    """
    df = pd.read_sql_query(query, db_engine)
    assert not df.empty, "Salary country query returned no results"
    assert "avg_salary" in df.columns
    assert df["avg_salary"].notnull().all()


def test_technology_language_query(db_engine):
    """Validates language popularity query returns ordered results."""
    query = """
        SELECT language_name, COUNT(*) AS count
        FROM respondent_languages
        WHERE survey_year = 2024
        GROUP BY language_name
        ORDER BY count DESC
    """
    df = pd.read_sql_query(query, db_engine)
    assert not df.empty, "Language popularity query returned no results"
    assert df["count"].iloc[0] >= df["count"].iloc[-1], "Results should be in descending order"


def test_cloud_adoption_query(db_engine):
    """Validates cloud provider adoption query returns expected fields."""
    query = """
        SELECT cloud_name, COUNT(DISTINCT respondent_id) AS user_count
        FROM respondent_cloud
        WHERE survey_year = 2024
        GROUP BY cloud_name
        ORDER BY user_count DESC
    """
    df = pd.read_sql_query(query, db_engine)
    assert not df.empty, "Cloud adoption query returned no results"
    assert "cloud_name" in df.columns
    assert "user_count" in df.columns


def test_ai_adoption_query(db_engine):
    """Validates AI tool usage query returns non-empty results for 2023-2024."""
    query = """
        SELECT ai_tool_name, COUNT(*) AS usage_count
        FROM respondent_ai_tools
        GROUP BY ai_tool_name
        ORDER BY usage_count DESC
    """
    df = pd.read_sql_query(query, db_engine)
    assert not df.empty, "AI adoption query returned no results"
    assert "ai_tool_name" in df.columns


def test_career_satisfaction_query(db_engine):
    """Validates job satisfaction cross-tabulation query."""
    query = """
        SELECT remote_work_mode, job_satisfaction, COUNT(*) AS dev_count
        FROM respondents
        WHERE survey_year = 2024
        GROUP BY remote_work_mode, job_satisfaction
        ORDER BY dev_count DESC
    """
    df = pd.read_sql_query(query, db_engine)
    assert not df.empty, "Career satisfaction query returned no results"
    assert "dev_count" in df.columns


def test_job_postings_query(db_engine):
    """Validates job postings salary aggregation query."""
    query = """
        SELECT job_title, COUNT(*) AS posting_count,
               AVG(offered_salary_max_usd) AS avg_max_salary
        FROM job_postings
        GROUP BY job_title
        ORDER BY avg_max_salary DESC
    """
    df = pd.read_sql_query(query, db_engine)
    assert not df.empty, "Job postings query returned no results"
    assert df["posting_count"].sum() > 0


def test_multi_year_trend_query(db_engine):
    """Validates multi-year language trajectory query returns all 4 years."""
    query = """
        SELECT survey_year, language_name, COUNT(*) AS count
        FROM respondent_languages
        WHERE language_name = 'Python'
        GROUP BY survey_year, language_name
        ORDER BY survey_year
    """
    df = pd.read_sql_query(query, db_engine)
    assert len(df) == 4, f"Expected 4 survey year rows for Python, got {len(df)}"
    assert set(df["survey_year"].tolist()) == {2021, 2022, 2023, 2024}


def test_skill_diversity_query(db_engine):
    """Validates skill diversity index computation."""
    query = """
        SELECT experience_bucket,
               AVG(skill_diversity_index) AS avg_diversity
        FROM respondents
        WHERE survey_year = 2024
        GROUP BY experience_bucket
    """
    df = pd.read_sql_query(query, db_engine)
    assert not df.empty, "Skill diversity query returned no results"
    assert (df["avg_diversity"] >= 0).all()
