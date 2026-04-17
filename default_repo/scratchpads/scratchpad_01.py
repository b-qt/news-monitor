"""
NOTE: Scratchpad blocks are used only for experimentation and testing out code.
The code written here will not be executed as part of the pipeline.
"""
from mage_ai.data_preparation.variable_manager import get_variable
import pandas as pd
from sqlalchemy import create_engine
import duckdb

df = get_variable('news_monitor', 'insert_and/or_create_new_columns', 'output_0')

# 1. Setup your file path (Using the absolute Docker path we fixed earlier)
db_path = '/home/src/data/news_db.duckdb'
table_name = 'spain_news_monitor'

# 2. Get the DDL (The "Blueprint")
# We use a temporary SQLite engine because its syntax is 99% identical 
# to DuckDB for standard CREATE TABLE statements.
temp_engine = create_engine('sqlite:///')
create_statement = pd.io.sql.get_schema(df, table_name, con=temp_engine)

print(f"""
--- 📜 THE BLUEPRINT --- 
{create_statement}
""")