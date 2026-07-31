"""
DevScope - Future Skills Forecast Engine Unit Tests
Validates 2-3 year projection outputs, growth category labels, and CAGR plausibility.
"""

import pytest
import pandas as pd
from analysis.forecast_engine import generate_skills_forecast


@pytest.fixture(scope="module")
def forecast_df():
    return generate_skills_forecast(forecast_years=3)


def test_forecast_returns_dataframe(forecast_df):
    """Forecast engine should return a non-empty DataFrame."""
    assert isinstance(forecast_df, pd.DataFrame)
    assert not forecast_df.empty


def test_forecast_expected_columns(forecast_df):
    """Forecast DataFrame must contain all required output columns."""
    required_cols = {
        "technology",
        "actual_2024_mentions",
        "projected_2026_mentions",
        "projected_2027_mentions",
        "historical_cagr_pct",
        "projected_category"
    }
    assert required_cols.issubset(set(forecast_df.columns)), (
        f"Missing columns: {required_cols - set(forecast_df.columns)}"
    )


def test_forecast_projected_counts_positive(forecast_df):
    """All projected mention counts must be positive integers."""
    assert (forecast_df["projected_2026_mentions"] > 0).all()
    assert (forecast_df["projected_2027_mentions"] > 0).all()


def test_forecast_category_labels_valid(forecast_df):
    """Projected category must only contain valid business labels."""
    valid_labels = {"High Growth", "Stable", "Declining"}
    actual_labels = set(forecast_df["projected_category"].unique())
    assert actual_labels.issubset(valid_labels), (
        f"Invalid forecast categories found: {actual_labels - valid_labels}"
    )


def test_high_growth_technologies_present(forecast_df):
    """At least one 'High Growth' technology should be projected."""
    high_growth = forecast_df[forecast_df["projected_category"] == "High Growth"]
    assert len(high_growth) >= 1, "Expected at least one High Growth technology"


def test_forecast_cagr_plausible_range(forecast_df):
    """CAGR values must be within a plausible range (-50% to +150%)."""
    assert (forecast_df["historical_cagr_pct"] >= -50).all()
    assert (forecast_df["historical_cagr_pct"] <= 150).all()
