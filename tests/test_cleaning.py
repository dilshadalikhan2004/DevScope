"""
DevScope - Data Cleaning Unit Tests
"""

import pytest
import numpy as np
from etl.clean import clean_experience_string, clean_compensation

def test_clean_experience_string():
    assert clean_experience_string("Less than 1 year") == 0.5
    assert clean_experience_string("More than 50 years") == 50.0
    assert clean_experience_string("10") == 10.0
    assert np.isnan(clean_experience_string("-5"))
    assert np.isnan(clean_experience_string("invalid"))

def test_clean_compensation():
    assert clean_compensation(100000) == 100000.0
    assert np.isnan(clean_compensation(500))  # Under minimum threshold
    assert np.isnan(clean_compensation(3000000))  # Outlier
