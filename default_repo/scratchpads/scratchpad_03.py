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
        title, 
        sentiment_label, 
        sentiment_score 
    FROM news 
    WHERE sentiment_label = 'Negative'
    ORDER BY sentiment_score DESC
    LIMIT 10
"""

results_df = pd.read_sql(query, con=engine)

print("---- SQL QUERY RESULTS ----")
print(results_df)