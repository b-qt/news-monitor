import streamlit as st
import pandas as pd
import os
import time             
import duckdb
import subprocess
import traceback # For debugging purposes, can be removed in production

# --- CONFIGURATION & PATHS ---
# We use absolute paths to ensure the Docker bouncer never gets lost
DB_PATH = "/home/src/data/news_db.duckdb" #"/home/src/data/news_report.duckdb"
DBT_DIR = "/home/src/news_report"

# --- ENGINE FUNCTIONS (The Logic) ---

def get_warehouse_data():
    """Attempt to load the refined data. Returns empty DF if table doesn't exist."""
    if not os.path.exists(DB_PATH):
        st.warning(f"⚠️ Database file not found at {DB_PATH}. The refinery needs to be started.")
        return pd.DataFrame()
    
    conn = duckdb.connect(database=DB_PATH, read_only=True)
    try:
        # We query the final 'Gold' Mart
        st.toast(f"👷‍♂️ Checking for refined data in database {DB_PATH.split('/')[-1]} ...")
        
        with st.spinner("⛏️ Mining the warehouse for insights...", 
                   show_time=True):
            st.toast("🔍 Running a quick check for available tables...")
            tables = conn.execute("SHOW TABLES").fetchall()
            
            #st.write(f"📦 Available tables in the warehouse: {' ; '.join(item[0] for item in tables)}")
            
            cmd_duckdb = "SELECT * FROM main.spain_news_feed  where published >= current_date - interval '2 months' ORDER BY published DESC" # We only want recent news for the dashboard, but this can be adjusted as needed
            #st.code(f"SQL Query: {cmd_duckdb}", language="sql")

            df = conn.execute(cmd_duckdb).df()
            st.toast(f"✅ {len(df)} rows retrieved successfully!")
            
            # Clear the screen of all messages
            st.empty()
        
            return df
    except:
        st.warning("⚠️ No refined data found. The refinery needs to be started.")
        st.error(traceback.format_exc()) # For debugging, can be removed in production
        return pd.DataFrame()
    finally:
        st.toast("🔒 Closing database connection.")
        conn.close()

def trigger_dbt_refinery():
    """The 'Chef' function: Distills raw files into the Gold warehouse."""
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = DBT_DIR
    env["DB_PATH"] = DB_PATH 
    
    # We use 'dbt build' to ensure Purity (Models + Tests)
    cmd = f'cd "{DBT_DIR}" && dbt build'
    
    with st.spinner("🏗️ Distilling daily files into the refinery..."):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
        return result.returncode == 0, result.stderr

# --- PRESENTATION FUNCTIONS (The UI) ---

def render_initialization_screen():
    """UI for when the warehouse is empty."""
    st.header("🇪🇸 Spain News Monitor")
    st.warning("📭 The warehouse is empty. The refinery needs to be started.")
    
    if st.button("🚀 Start dbt Refinery"):
        success, error_msg = trigger_dbt_refinery()
        if success:
            st.success("✅ Success! Data distilled. Handshaking with UI...")
            time.sleep(1)
            # 🚀 THE CRITICAL MOVE: Force a full script re-run
            st.rerun()
        else:
            st.error("The bouncer blocked the refinery run.")
            st.code(error_msg)

def render_analytics_dashboard(df):
    """UI for the high-purity news market insights."""
    page_setup = {
        "page_title": "Northern Spain News Market Refinery",
        "page_icon": "🏙️",
        "layout": "wide"
    }
    st.set_page_config(**page_setup)
    st.title("🏙️ Northern Spain News Market Refinery")
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total News", len(df))
    m2.metric("Top Paper", df['source'].mode()[0] if 'source' in df.columns else "N/A")
    m3.metric("Last Update", time.strftime("%H:%M"))

    st.divider()
    
    # Data Table
    st.subheader(":newspaper: Refined News Feed")
    st.dataframe(
        df[["title", "link", "source", "sentiment_label", "category"]].sample(n=5),
        use_container_width=True, 
        hide_index=True,
        column_config={
        "link": st.column_config.LinkColumn("Read Article"),
        "source": "📰 Source",
        "sentiment_label": "📊 Sentiment",
        "title": "🗞️ Title",
        "category": "Category"
    })
    
    sentiment_order = ['NEG', 'NEU', 'POS']
    colors = ['#E74C3C', '#3498DB', '#2ECC71'] # Red (Neg), Blue (Neu), Green (Pos)

    st.header("📊 Daily Sentiment Trends")
    cols = st.columns(3)

    for i, cat in enumerate(['economy', 'tech', 'real_estate']):
        with cols[i]:
            st.subheader(cat.title())
            
            cat_df = df[df['category'] == cat]
            if not cat_df.empty:
                chart_data = (
                    cat_df.groupby([df['published'].dt.date, 'sentiment_label'])
                    .size()
                    .unstack(fill_value=0)
                    )
                for label in sentiment_order:
                    if label not in chart_data.columns:
                        chart_data[label] = 0
                chart_data = chart_data[sentiment_order].sort_index()
                st.bar_chart(chart_data, color=colors, horizontal=True)
            else:
                st.info("📭 No data.")
            
    # Sidebar for Warehouse Management
    with st.sidebar:
        st.subheader("🛠️ Maintenance")
        if st.button("🗑️ Clear Cache & Refresh"):
            st.cache_data.clear()
            st.rerun()

# --- THE ORCHESTRATOR ---

def app_orchestrator():
    """Determines which reality to show the user based on database state."""
    # 1. Check the Fridge
    data = get_warehouse_data()
    
    # 2. Decision Tree
    if data.empty:
        render_initialization_screen()
    else:
        render_analytics_dashboard(data)

def main():
    """Main entry point - implementation of the render loop."""
    # st.set_page_config is already called at module level 
    # to avoid the 'Bouncer Error'
    app_orchestrator()

if __name__ == '__main__':
    main()