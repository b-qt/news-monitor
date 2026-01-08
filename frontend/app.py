import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import glob
import os
import duckdb

# 1. Pro-Tip: Cache the data so the app stays snappy
@st.cache_data(show_spinner="Cleaning the fridge and removing duplicates...") 
def load_data():
    """Load, merge, and deduplicate news data."""
    db_file_pattern = os.getenv("DB_FILE_PATH", '/home/src/data/*.duckdb')
    db_files = glob.glob(db_file_pattern)
    
    if not db_files:
        return pd.DataFrame()
    
    # 1. Use a list to collect dataframes (Way faster than pd.concat in a loop)
    df_list = []
    
    for file_path in db_files:
        with st.status(f"Checking {os.path.basename(file_path)}...", expanded=False) as status:
            try:
                # 2. Optimization: Use DuckDB's native connection (No SQLAlchemy overhead)
                # We use 'SELECT DISTINCT' right at the source to save memory
                conn = duckdb.connect(file_path, read_only=True)
                query = "SELECT DISTINCT * FROM spain_news_monitor"
                df = conn.execute(query).df()
                conn.close()
                
                if not df.empty:
                    df_list.append(df)
                    status.update(label=f"✅ Found {len(df)} unique records", state="complete")
            except Exception as e:
                st.error(f"Error reading {file_path}: {e}")

    if not df_list:
        return pd.DataFrame()

    # 3. Combine everything once
    full_df = pd.concat(df_list, ignore_index=True)

    # 4. Global Deduplication
    # We use the 'link' column as the unique ID. If 'link' is missing, use 'title'.
    # We keep the 'first' instance found.
    dedup_column = 'link' if 'link' in full_df.columns else 'title'
    
    initial_count = len(full_df)
    full_df = full_df.drop_duplicates(subset=[dedup_column], keep='first')
    final_count = len(full_df)
    
    if initial_count > final_count:
        st.toast(f"🗑️ Removed {initial_count - final_count} duplicate articles!")

    # 5. Final Sort: Most recent news first
    if 'published_date' in full_df.columns:
        full_df['published_date'] = pd.to_datetime(full_df['published_date'])
        full_df = full_df.sort_values(by='published_date', ascending=False)

    return full_df

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
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ3bmZ3bmZ3/3o7TKMGpxx6B8N8W6/giphy.gif")
        st.warning("👨‍🍳 The Chef (Mage AI) is currently fetching the first batch of news. This takes about 2-3 minutes...")
        if st.button("Check if the Chef is finished"):
            st.rerun()
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