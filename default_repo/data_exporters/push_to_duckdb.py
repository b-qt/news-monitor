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
    today = pd.Timestamp.now().date()
    db_path = f'/home/src/data/news_db_{today}_.duckdb'
    table_name = 'spain_news_monitor'

    temp_engine = create_engine('sqlite:///')
    create_statement = pd.io.sql.get_schema(df, table_name, con=temp_engine)
    print(f"""
        --- 📜 THE BLUEPRINT --- 
        {create_statement}
        """)

    # 3. Insert into DuckDB 
    # Create the file if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    # We'll use the native duckdb library here because it's faster and 
    # handles pandas DataFrames like a dream.
    conn = duckdb.connect(db_path)

    try:
        # Option A: Create table using the statement we just generated
        # (We use 'IF NOT EXISTS' to avoid Reyes Magos drama)
        clean_statement = create_statement.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
        conn.execute(clean_statement)

        # Option B: Insert the data
        # DuckDB is magic: it can 'register' a pandas DF and query it directly
        conn.execute(f"INSERT INTO {table_name} SELECT * FROM df")

        print(f"✅ Success! Data gifted to {table_name} in {os.path.basename(db_path)}.")
    except Exception as e:
        print(f"❌ The coal in the stocking: {e}")
    finally: 
        conn.close()