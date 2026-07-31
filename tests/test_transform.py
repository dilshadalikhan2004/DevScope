"""
DevScope - Feature Engineering Unit Tests
"""

import pytest
from etl.transform import derive_experience_bucket, derive_salary_band

def test_derive_experience_bucket():
    assert derive_experience_bucket(1.0) == "0-2 years (Entry)"
    assert derive_experience_bucket(4.0) == "3-5 years (Mid)"
    assert derive_experience_bucket(8.0) == "6-10 years (Senior)"
    assert derive_experience_bucket(15.0) == "11+ years (Lead/Executive)"

def test_derive_salary_band():
    assert derive_salary_band(45000) == "Entry (<$50k)"
    assert derive_salary_band(75000) == "Mid ($50k-$100k)"
    assert derive_salary_band(120000) == "High ($100k-$180k)"
    assert derive_salary_band(200000) == "Top 10% (>$180k)"
