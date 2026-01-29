import streamlit as st

import pandas as pd

import glob
import os

import time             
import duckdb

#from sqlalchemy import create_engine


#@st.cache_data(show_spinner=False) # Spinner is handled by our manual status
def load_whole_data(db_path: str) -> pd.DataFrame:
    """Read data after it has been processed in dbt"""
    if not os.path.exists(db_path):
        st.error(f"🚫 File not found in: {db_path}")
        return pd.DataFrame()
    
    #2 . Create connection engine in read-only mode
    conn = duckdb.connect(database=db_path, 
                          read_only=True)
    
    try:
        #3. Read data into pandas dataframe from mart or incremental table
        query = """
        SELECT * FROM spain_snapshot.spain_news_snapshot
        ORDER BY published DESC
        """
    
        df = conn.execute(query).df()
        df = df.drop(
            [
                #'sentiment_label',
                'sentiment_score',
                'entry_date',
                'dbt_updated_at',
                'news_id',
                'dbt_valid_from',
                'dbt_valid_to',
                'published',
                'dbt_scd_id'
            ], 
            axis=1
        )
    except Exception as e:
        st.error(
            f"Database error: {e}"
        )
    finally:
        #4. Close connection
        conn.close()
    return df

def load_daily_data(db_path:str) -> pd.DataFrame:
    if not os.path.exists(db_path):
        st.error(f"🚫 File not found in: {db_path}")
        return pd.DataFrame()
    conn = duckdb.connect(database = db_path, 
                          read_only=True)
    try:
        
        query = """
        select * from main.fct_daily_sentiment
        """
        
        df = conn.execute(query).df()
        
        if not df.empty:
            st.toast(f"Data loaded! Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        else:
            st.warning(
                "Connected successfully, but 'fct_daily_sentiment' is empty "
            )
    except Exception as e:
        st.error(
            f"Database Error: {e}"
        )
        actual_tables = conn.execute(
            "show tables"
        ).df()
        st.write(
            "Tables actually found:",
            actual_tables
        )
        df = pd.DataFrame()
    finally:
        conn.close()
    
    return df
    
    

def page_setup(db_path: str):
    
    data_raw = load_whole_data(db_path=DB_PATH) #---- hide a column from data
    daily_sentiment_data = load_daily_data(db_path)
    
    
    st.set_page_config(page_title="Spain News Monitor 2026", page_icon="🇪🇸", layout="wide")    
    st.write("# 🇪🇸 Spain News Monitor Application")
    
    
    if data_raw.empty:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ3bmZ3bmZ3/3o7TKMGpxx6B8N8W6/giphy.gif")
        st.warning("👨‍🍳 The Chef (Mage AI) is currently fetching the first batch of news. This takes about 2-3 minutes...")
        # Added a timer to show when it last checked
        st.caption(f"Last checked: {time.strftime('%H:%M:%S')}")
        if st.button("Check if the Chef is finished"):
            st.rerun()
        return
    
    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col3.metric("Total Articles", len(data_raw))
    
    # Safe access to columns
    u_sources = data_raw['source'].nunique() if 'source' in data_raw.columns else 0
    col2.metric("Unique Sources", u_sources)
    
    # Date Range
    if 'entry_display' in data_raw.columns:
        date_range = f"{data_raw['entry_display'].min()} - {data_raw['entry_display'].max()}"
        col1.metric("Date Range", date_range)
    
    st.divider()
    
    # Display Results
    st.dataframe(data_raw.sample(10), 
                 width='content',
                 hide_index=True,
                 )
    
    if 'sentiment' in daily_sentiment_data.columns:
        st.write(f"### 📊 Public Sentiment for the week")
        st.dataframe(daily_sentiment_data.head(),
                     width="content",
                     hide_index=True)
        
        #-------
        st.subheader(f"### 📊 Public Sentiment for the week")

        # 1. Pivot the data: Rows = Dates, Columns = Sentiments
        # This is what st.bar_chart expects for grouping
        pivot_data = daily_sentiment_data.pivot(
            index='date_display', 
            columns='sentiment', 
            values='number_of_articles'
        ).fillna(0) # Fill days with no news with 0

        st.bar_chart(pivot_data,
                     horizontal=True)
    else:
        st.write("Sentiment label not found int daily data")
        
    # Sidebar
    with st.sidebar:
        st.divider()
        st.subheader(" Warehouse health")
        
        db_size = os.path.getsize(db_path) / (1024 * 1024)
        st.metric("DuckDB Size (MB)", f"{db_size:.2f} MB")
        
        if st.button("Refresh Data"):
           conn = duckdb.connect(database=db_path, 
                                 read_only=True)
           count = conn.execute(
               "SELECT COUNT(*) FROM spain_snapshot.spain_news_snapshot"
               ).fetchone()[0]
           conn.close()
           st.write(f"Total records in the database: {count}")
           
    
if __name__ == '__main__':
    #1. Point to DuckDB database
    DB_PATH = "data/news_report.duckdb"

    try:
        pipelines = os.listdir('/home/src/default_repo/pipelines/')
        print(f"\t\t\t\tDEBUG: Found pipelines: {pipelines}")
    except Exception as e:
        print(f"\t\t\t\tDEBUG Error accessing pipelines: {e}")
    page_setup(db_path=DB_PATH)