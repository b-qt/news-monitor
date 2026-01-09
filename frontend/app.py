import streamlit as st
import pandas as pd
import glob
import os
import time             
import duckdb
from sqlalchemy import create_engine

#@st.cache_data(show_spinner=False) # Spinner is handled by our manual status
def load_data():
    """Load, merge, and deduplicate news data."""
    # Ensure we look in the correct Docker folder
    db_file_pattern = '/home/src/data/*.duckdb'
    db_files = glob.glob(db_file_pattern)
    
    if not db_files:
        print("DEBUG: No .duckdb files found in /home/src/data/")
        return pd.DataFrame()
    
    df_list = []
    
    for file_path in db_files:
        status_placeholder = st.empty()
        with status_placeholder.status(f"Reading {os.path.basename(file_path)}...", expanded=False) as status:
            try:
                # Use native DuckDB for speed on Hugging Face
                conn = duckdb.connect(file_path, read_only=True)
                # Matches the table name from your Mage Exporter
                query = "SELECT * FROM spain_news_monitor"
                df = conn.execute(query).df()
                conn.close()
                
                if not df.empty:
                    df_list.append(df)
                    status.update(label="File read successfully!", state="complete")
                    time.sleep(0.5)
                    status_placeholder.empty()
                    st.toast(f"✅ Loaded {len(df)} items from {os.path.basename(file_path)}", icon="📰")

            except Exception as e:
                status_placeholder.empty()
                print(f"DEBUG Error: {e}")
                st.error(f"Error reading {file_path}")

    if not df_list:
        return pd.DataFrame()

    full_df = pd.concat(df_list, ignore_index=True)

    # 1. FIX: Use 'link' or 'title' for deduplication
    id_col = 'link' if 'link' in full_df.columns else 'title'
    full_df = full_df.drop_duplicates(subset=[id_col], keep='first')

    # 2. FIX: Unified Column Mapping
    # Ensure column names match what Mage produces
    rename_map = {'source': 'source', 'published': 'published'}
    full_df = full_df.rename(columns={k: v for k, v in rename_map.items() if k in full_df.columns})

    if 'published' in full_df.columns:
        full_df['published'] = pd.to_datetime(full_df['published'])
        full_df = full_df.sort_values(by='published', ascending=False)

    return full_df

def page_setup():
    st.set_page_config(page_title="Spain News Monitor 2026", page_icon="🇪🇸", layout="wide")    
    st.write("# 🇪🇸 Spain News Monitor Application")
    
    data = load_data()
    
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
    
    if 'published' in data.columns:
        date_range = f"{data['published'].min().strftime('%d %b')} to {data['published'].max().strftime('%d %b')}"
        col3.metric("Date Range", date_range)
    
    st.divider()
    
    # Display Results
    st.dataframe(data.sample(25), 
                 width='content',
                 hide_index=True)
    
    if 'sentiment_label' in data.columns:
        st.write("### 📊 Public Sentiment")
        st.bar_chart(data['sentiment_label'].value_counts())
    
if __name__ == '__main__':
    try:
        pipelines = os.listdir('/home/src/.mage/pipelines/')
        print(f"\t\t\t\tDEBUG: Found pipelines: {pipelines}")
    except Exception as e:
        print(f"\t\t\t\tDEBUG Error accessing pipelines: {e}")
    page_setup()