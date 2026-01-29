{% snapshot sagrada_sentiment_snapshot %}
  {{
    config(
        target_schema='sagrada_snapshots', 
        target_database='news_report', 
        unique_key='news_id', 
        strategy='timestamp', 
        updated_at='entry_date', 
    )
  }}

  /*
    - target_schema: 'sagrada_snapshots' specifies the schema where the snapshot data will be stored.
    - target_database: 'news_report' specifies the database where the snapshot data will be stored
    - unique_key: 'link' is used to uniquely identify each news article.
    - strategy: 'timestamp' indicates that the snapshot will track changes based on a timestamp column.
    - updated_at: 'entry_date' is the column that indicates when the record was last updated ...
                  which triggers the snapshot to capture a new version of the record. 
   */

  select * from {{ ref('ephemeral_spain_news') }} -- snapshot source data
  where title ILIKE '%sagrada familia%'
{% endsnapshot %}

---  Snapshot to track sentiment changes in news articles about Sagrada Familia over time. ---
---  This snapshot captures all changes over time based on the entry_date timestamp.
---  It uses the 'link' as the unique key to identify each article.
---  The snapshot is stored in the 'sagrada_snapshots' schema within the 'news_report' database.
---  The snapshot is triggered by changes in the 'entry_date' column; 
---  so any update to this column will create a new version of the record.
---        Last updated: 2024-06-10        ---
--- To look at the snapshot, use: dbt show --select sagrada_sentiment_snapshot ---
--- To build the snapshot, use: dbt snapshot --select sagrada_sentiment_snapshot ---