"""
DevScope - Database Initialization & Population Script
Executes schema creation DDL, triggers data loader, and applies indexing rules.
"""

from sqlalchemy import create_engine, text
from config import SQLALCHEMY_DATABASE_URI, DATABASE_DIR
from etl.logger import get_logger
from etl.load import load_data_to_database

logger = get_logger(__name__)

def initialize_database():
    """Applies schema DDL, loads data, and builds indexes."""
    logger.info("Initializing DevScope Database Schema...")
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    schema_path = DATABASE_DIR / "schema.sql"
    indexes_path = DATABASE_DIR / "indexes.sql"
    
    with open(schema_path, "r") as f:
        schema_sql = f.read()
        
    with engine.connect() as conn:
        for statement in schema_sql.split(";"):
            if statement.strip():
                conn.execute(text(statement))
        conn.commit()
    logger.info("Schema DDL applied successfully.")
    
    # Load data
    load_data_to_database(SQLALCHEMY_DATABASE_URI)
    
    # Apply indexes
    with open(indexes_path, "r") as f:
        indexes_sql = f.read()
        
    with engine.connect() as conn:
        for statement in indexes_sql.split(";"):
            if statement.strip():
                conn.execute(text(statement))
        conn.commit()
    logger.info("Database indexes built successfully.")

if __name__ == "__main__":
    initialize_database()
