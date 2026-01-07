"""
NOTE: Scratchpad blocks are used only for experimentation and testing out code.
The code written here will not be executed as part of the pipeline.
"""
df = get_variable('news_monitor', 'insert_and/or_create_new_columns', 'output_0')

# Create engine
engine = create_engine('sqlite:///')

# 3. CREATE the table and LOAD the data 
df.to_sql('news', con=engine, index=False, if_exists='replace')

# 4. RUN your SQL query
query = """
    SELECT 
        sentiment_label, 
        sentiment_score
    FROM news 
    GROUP BY sentiment_label
    LIMIT 20
"""

results_df = pd.read_sql(query, con=engine)

print("---- GENERAL SENTIMENT RESULTS ----")
print(results_df)