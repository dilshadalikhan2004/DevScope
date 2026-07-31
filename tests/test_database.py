"""
DevScope - Database Schema Integration Tests
"""

import pytest
import pandas as pd
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI

def test_database_tables_exist():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    df_resp = pd.read_sql_query("SELECT COUNT(*) AS total FROM respondents", engine)
    assert df_resp.iloc[0]["total"] > 0

    df_jobs = pd.read_sql_query("SELECT COUNT(*) AS total FROM job_postings", engine)
    assert df_jobs.iloc[0]["total"] > 0
