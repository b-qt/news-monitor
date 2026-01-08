import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import glob
import os
import duckdb

# 1. Pro-Tip: Cache the data so the app stays snappy
@st.cache_data(show_spinner="Fetching news from the fridge...") 
def load_data():
    """ Load and return data for the application."""
    
    # FIX: Ensure we use the absolute Docker path
    db_file_pattern = os.getenv("DB_FILE_PATH", '/home/src/data/*.duckdb')
    db_files = glob.glob(db_file_pattern)
    
    if not db_files:
        # Don't use st.error here if you want a clean 'empty' state
        return pd.DataFrame()
    
    resulting_df = pd.DataFrame()
    
    for file_path in db_files:
        # Use status to show progress without cluttering the UI
        with st.status(f"Reading {os.path.basename(file_path)}...", expanded=False) as status:
            # FIX: Use 4 slashes for absolute path in duckdb-engine
            engine = create_engine(f'duckdb:///{file_path}')
            try:
                with engine.connect() as connection:
                    # Matches your Mage Exporter table name
                    query = "SELECT * FROM spain_news_monitor"
                    df = pd.read_sql(query, connection)
                    
                    resulting_df = pd.concat([resulting_df, df], ignore_index=True)
                    status.update(label=f"✅ Loaded {len(df)} records", state="complete")
                    
            except Exception as e:
                st.error(f"Error loading {file_path}: {e}")

    return resulting_df

def page_setup():
    # 2. FIX: This MUST be the first Streamlit command in the whole app
    st.set_page_config(
        page_title="Spain News Monitor 2026",
        page_icon="🇪🇸",
        layout="wide",
        initial_sidebar_state="collapsed",
    )    
    
    st.write("# 🇪🇸 Spain News Monitor Application")
    st.write("Real-time AI Sentiment Analysis of Spanish Headlines")
    
    # Load data
    data = load_data()
    
    if data.empty:
        st.info("👋 Welcome! The database is currently empty. Please run the Mage pipeline to fetch the first batch of news.")
        return
    
    # 3. FIX: Column Names (Matching your Transformer Block)
    # Mapping: 'source' -> 'source_name' | 'published' -> 'published_date'
    
    # Basic Data Cleaning for the UI
    if 'published' in data.columns:
        data['published'] = pd.to_datetime(data['published'])

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Articles", len(data))
    
    if 'source_name' in data.columns:
        col2.metric("Unique Sources", data['source'].nunique())
    
    if 'published_date' in data.columns:
        start_date = data['published'].min().strftime('%d %b')
        end_date = data['published'].max().strftime('%d %b')
        col3.metric("Date Range", f"{start_date} to {end_date}")
    
    # Display Sample Data
    st.divider()
    st.write("### 📋 Latest Headlines")
    
    # Select columns that actually exist to avoid KeyErrors
    display_cols = ['title', 'title_english', 'sentiment_label', 'source', 'published']
    existing_display_cols = [c for c in display_cols if c in data.columns]
    
    st.dataframe(
        data[existing_display_cols].sort_values(by=existing_display_cols[0], ascending=False).head(20),
        use_container_width=True,
        hide_index=True
    )
    
    # 4. FIX: Sentiment Chart
    if 'sentiment_label' in data.columns:
        st.write("### 📊 Overall Sentiment (Spanish Model)")
        # We use a color map to make it look professional
        sentiment_counts = data['sentiment_label'].value_counts()
        st.bar_chart(sentiment_counts)
    
def main():
    page_setup()
    
if __name__ == '__main__':
    main()