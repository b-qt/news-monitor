{% snapshot spain_news_snapshot %}
{{
    config(
        target_schema="spain_snapshot",
        target_database="news_report",
        unique_key='news_id',
        strategy='timestamp',
        updated_at='entry_date',
        invalidate_hard_deletes=True,

        snapshot_meta_column_names={
            "dbt_scd_id": "scd_id",
            "dbt_is_deleted": "is_deleted"
        }
    )
}}
select 
    news_id,
    title,
    link,
    sentiment_label,
    sentiment_score,
    source,
    published,
    cast(entry_date as date) as entry_date,
    {{ format_date('published') }} as published_display,
    {{ format_date('entry_date') }} as entry_display
from {{ ref('ephemeral_spain_news') }}
where link is not null
and trim(link) != ''
and lower(link) != 'none'

-- Remove duplicates based on link, keeping the most recent published date
{% set partition_cols = "link" %}
{% set order_by_col = "published desc" %}
{{ remove_duplicates(partition_cols, order_by_col) }}



{% endsnapshot %}

/* Snapshots are not mutable; you have to nuke it and rebuild it ...

    Created a macro to delete and rebuild the snapshots....
    1. pythonically >> 
        python3 -c "import duckdb; 
        conn = duckdb.connect('data/news_report.duckdb'); 
        conn.execute('DROP TABLE IF EXISTS spain_snapshot.spain_news_snapshot'); 
        conn.close(); 
        print('✅ Table Nuked.')" 
    2. macro >>>
        dbt run-operation drop_spain_snapshot

    then run dbt run --full-refresh; or trigger a run in mage
*/