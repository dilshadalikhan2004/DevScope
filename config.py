"""
DevScope - Configuration Module
Centralized configuration management for file paths, database URIs,
cleaning rules, KPI weightings, and logging setup.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DOCS_DIR = BASE_DIR / "docs"
REPORTS_DIR = BASE_DIR / "reports"
DASHBOARD_DIR = BASE_DIR / "dashboard"
SQL_DIR = BASE_DIR / "sql"
DATABASE_DIR = BASE_DIR / "database"

# Ensure directories exist
for directory in [RAW_DATA_DIR, CLEANED_DATA_DIR, PROCESSED_DATA_DIR, DOCS_DIR, REPORTS_DIR, DASHBOARD_DIR, SQL_DIR, DATABASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database Configuration
# Uses SQLite locally by default; falls back to PostgreSQL if ENV variable is set
DB_TYPE = os.getenv("DEVSCOPE_DB_TYPE", "sqlite")
SQLITE_PATH = DATABASE_DIR / "devscope.db"
POSTGRES_URI = os.getenv(
    "DEVSCOPE_POSTGRES_URI",
    "postgresql://postgres:postgres@localhost:5432/devscope"
)

if DB_TYPE == "postgresql":
    SQLALCHEMY_DATABASE_URI = POSTGRES_URI
else:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_PATH}"

# Datasets & Sources
SURVEY_YEARS = [2021, 2022, 2023, 2024]
PRIMARY_SURVEY_YEAR = 2024

RAW_SURVEY_PATHS = {
    year: RAW_DATA_DIR / f"survey_{year}.csv" for year in SURVEY_YEARS
}
RAW_JOB_POSTINGS_PATH = RAW_DATA_DIR / "tech_job_postings.csv"
RAW_GITHUB_TRENDS_PATH = RAW_DATA_DIR / "github_octoverse.csv"

CLEANED_COMBINED_PATH = CLEANED_DATA_DIR / "combined_surveys_2021_2024.csv"
CLEANED_JOB_POSTINGS_PATH = CLEANED_DATA_DIR / "job_postings_cleaned.csv"
PROCESSED_KPI_PATH = PROCESSED_DATA_DIR / "executive_kpis.json"

# Cleaning Parameters
MIN_VALID_AGE = 18
MAX_VALID_AGE = 85
MIN_VALID_EXPERIENCE = 0
MAX_VALID_EXPERIENCE = 60
MIN_COMPENSATION_USD = 1000
MAX_COMPENSATION_USD = 2500000

# Executive Composite KPI Weights
KPI_WEIGHTS = {
    "market_health": {
        "employment_rate": 0.4,
        "satisfaction_rate": 0.3,
        "compensation_parity": 0.3
    },
    "ai_readiness": {
        "ai_usage_rate": 0.5,
        "ai_favorable_sentiment": 0.3,
        "workflow_integration": 0.2
    },
    "remote_readiness": {
        "remote_rate": 0.6,
        "hybrid_rate": 0.4
    }
}

# Supported Currencies to USD Conversion Fallback Table (for survey responses)
CURRENCY_TO_USD = {
    "USD": 1.0,
    "EUR": 1.09,
    "GBP": 1.28,
    "CAD": 0.73,
    "AUD": 0.66,
    "INR": 0.012,
    "BRL": 0.18,
    "CHF": 1.13,
    "SGD": 0.74,
    "JPY": 0.0064
}

# Logging Configuration
LOG_LEVEL = os.getenv("DEVSCOPE_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
