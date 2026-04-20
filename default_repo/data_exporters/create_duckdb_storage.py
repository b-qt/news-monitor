from mage_ai.io.file import FileIO

import pandas as pd
from pandas import DataFrame

from sqlalchemy import create_engine

import duckdb

import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_file(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to filesystem.

    Docs: https://docs.mage.ai/design/data-loading#fileio
    """ 
    today = pd.to_datetime("today").date()
    #db_path = f'/home/src/data/news_db_{today}_.duckdb'
    db_path = f'/home/src/data/news_db.duckdb'
    db_dir = os.path.dirname(db_path)
    # Create the database file if it doesn't exist
    if not os.path.exists(db_path):
        os.makedirs(db_dir, exist_ok=True)
    
    conn = duckdb.connect(database=db_path, read_only=False)
    
    try:
        with duckdb.connect(database=db_path, read_only=False) as conn: # We use a context manager to ensure the connection is properly closed
            conn.register('df', df) # Register the DataFrame as a temporary table in DuckDB
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS spain_news_feed (
                    title TEXT,
                    link TEXT,
                    published DATE,
                    source TEXT,
                    entry_date DATE,
                    sentiment_label TEXT,
                    category TEXT
                );  
                        """)
            conn.execute("""
                        INSERT INTO spain_news_feed SELECT *  FROM df
                        """)
            print(f"Data exported successfully to {db_path}")
        
    except Exception as e:
        print(f"Error exporting data: {e}")
        raise e
    
    return None

@test
def check_db_exists(*args): 
    assert os.path.exists("home/src/data/news_db.duckdb"), "Database file was not created successfully."