import streamlit as st
import pandas as pd
import glob
import os
import time             
import duckdb
from sqlalchemy import create_engine

#@st.cache_data(show_spinner=False) # Spinner is handled by our manual status
def load_data(db_path: str) -> pd.DataFrame:
    """Read data after it has been processed in dbt"""
    if not os.path.exists(db_path):
        st.error(f"🚫 File not found in: {db_path}")
        return pd.DataFrame()
    
    #2 . Create connection engine in read-only mode
    conn = duckdb.connect(database=db_path, 
                          read_only=True)
    #3. Read data into pandas dataframe from mart or incremental table
    query = """
    SELECT * FROM main.stg_news_incremental
    ORDER BY published DESC
    """
    
    df = conn.execute(query).df()
    #4. Close connection
    conn.close()
    return df
    

def page_setup(db_path: str):
    st.set_page_config(page_title="Spain News Monitor 2026", page_icon="🇪🇸", layout="wide")    
    st.write("# 🇪🇸 Spain News Monitor Application")
    
    data = load_data(db_path=DB_PATH)
    
    if data.empty:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ3bmZ3bmZ3/3o7TKMGpxx6B8N8W6/giphy.gif")
        st.warning("👨‍🍳 The Chef (Mage AI) is currently fetching the first batch of news. This takes about 2-3 minutes...")
        # Added a timer to show when it last checked
        st.caption(f"Last checked: {time.strftime('%H:%M:%S')}")
        if st.button("Check if the Chef is finished"):
            st.rerun()
        return
    
    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Articles", len(data))
    
    # Safe access to columns
    u_sources = data['source'].nunique() if 'source' in data.columns else 0
    col2.metric("Unique Sources", u_sources)
    
    # Date Range
    if 'entry_date' in data.columns:
        date_range = f"{data['entry_date'].min().strftime('%d %b')} to {data['entry_date'].max().strftime('%d %b')}"
        col3.metric("Date Range", date_range)
    
    st.divider()
    
    # Display Results
    st.dataframe(data.sample(25), 
                 width='content',
                 hide_index=True)
    
    if 'sentiment_label' in data.columns:
        st.write("### 📊 Public Sentiment")
        st.bar_chart(data['sentiment_label'].value_counts(),
                     use_container_width=True)
        
    # Sidebar
    with st.sidebar:
        st.divider()
        st.subheader(" Warehouse health")
        
        db_size = os.path.getsize(db_path) / (1024 * 1024)
        st.metric("DuckDB Size (MB)", f"{db_size:.2f} MB")
        
        if st.button("Refresh Data"):
           # st.experimental_rerun()
           conn = duckdb.connect(database=db_path, 
                                 read_only=True)
           count = conn.execute("SELECT COUNT(*) FROM main.stg_news_incremental").fetchone()[0]
           conn.close()
           st.write(f"Total records in the database: {count}")
    
if __name__ == '__main__':
    #1. Point to DuckDB database
    DB_PATH = "data/news_report.duckdb"

    try:
        pipelines = os.listdir('/home/src/.mage/pipelines/')
        print(f"\t\t\t\tDEBUG: Found pipelines: {pipelines}")
    except Exception as e:
        print(f"\t\t\t\tDEBUG Error accessing pipelines: {e}")
    page_setup(db_path=DB_PATH)