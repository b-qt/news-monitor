import streamlit as st

import pandas as pd

from sqlalchemy import create_engine

import glob
import os

@st.cache_data(show_spinner=True) # Cache the loaded data to improve performance
def load_data():
    """ Load and return data for the application."""
    
    # Connect to the duckdb database file
    db_file_path = os.getenv("DB_FILE_PATH", '/home/src/data/*.duckdb')
    db_files = glob.glob(db_file_path)
    if not db_files:
        st.error("🔍 No database files found.")
        return pd.DataFrame()
    
    # read data from all files matching the pattern
    resulting_df = pd.DataFrame()
    
    for file_path in db_files:
        with st.status(f"Loading data from {file_path}...", expanded=False) as status:
            engine = create_engine(f'duckdb:///{file_path}')
            try:
                with engine.connect() as connection:
                    query = "SELECT * FROM spain_news_monitor"
                    df = pd.read_sql(query, connection)
                    
                    resulting_df = pd.concat([resulting_df, df], ignore_index=True)
                    #st.success(f"Loaded {len(df)} records from {file_path}")
                    status.update(f"Loaded {len(df)} records from {file_path}", 
                                  state="success")
                    
            except Exception as e:
                st.error(f"Error loading data from {file_path}: {e}")

    return resulting_df

def test_data_loaded() -> None:
    data = load_data()
    assert "message" in data
    assert data["message"] == "Data loaded successfully."

def page_setup():
    st.set_page_config(
        page_title="News Monitor",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )    
    st.write("# News Monitor Application")
    
    # Load data
    data = load_data()
    if data.empty:
        st.warning("No data available to display.")
        return
    
    st.write(f"Data loaded with {len(data)} records.")
    #st.write(f"Data columns: {data.columns.tolist()}")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Articles", len(data))
    col2.metric("Unique Sources", data['source'].nunique())
    col3.metric("Date Range", f"{data['published'].min()} to {data['published'].max()}")
    
    # Display first few records
    st.write("### Sample Data")
    st.dataframe(data.sample(10),
                 use_container_width=True)
    
    # Sentiment Chart
    st.bar_chart(data['sentiment_label'].value_counts())
    
def main():
    page_setup()
    
if __name__ == '__main__':
    main()