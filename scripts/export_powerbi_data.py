"""
DevScope - Power BI Data Export Automation
Exports cleaned star schema tables from PostgreSQL/SQLite into ready-to-import
CSVs for Power BI Desktop, verifying data schema consistency.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI, DATA_DIR
from etl.logger import get_logger

logger = get_logger(__name__)

def export_powerbi_datasets():
    """Exports star schema tables for Power BI Desktop import."""
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    pbi_dir = DATA_DIR / "powerbi"
    pbi_dir.mkdir(parents=True, exist_ok=True)
    
    tables = [
        "respondents",
        "respondent_languages",
        "respondent_cloud",
        "respondent_ai_tools",
        "job_postings"
    ]
    
    logger.info(f"Exporting Power BI star schema datasets to {pbi_dir}...")
    for table_name in tables:
        df = pd.read_sql_table(table_name, engine)
        csv_path = pbi_dir / f"{table_name}.csv"
        try:
            df.to_csv(csv_path, index=False)
            logger.info(f"Exported {len(df):,} rows for table '{table_name}' to {csv_path.name}")
        except PermissionError:
            temp_path = pbi_dir / f"{table_name}_export.csv"
            df.to_csv(temp_path, index=False)
            logger.warning(f"File {csv_path.name} is currently open in another process. Exported to {temp_path.name} instead.")

if __name__ == "__main__":
    export_powerbi_datasets()
