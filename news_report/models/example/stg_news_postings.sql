{{ config(materialized='incremental', unique_key='link') }}

{# 1. Find all daily files, but EXCLUDE the main report file to avoid recursion #}
{% set find_files_query %}
    SELECT file FROM glob('/home/src/data/news_db_*.duckdb')
{% endset %}

{% set results = run_query(find_files_query) %}

{% if execute %}
    {% set db_files = results.columns[0].values() %}
    {% for file in db_files %}
        {% set alias = "daily_" ~ loop.index0 %}
        {# We attach each daily file as a separate room #}
        {% do run_query("ATTACH '" ~ file ~ "' AS " ~ alias ~ " (READ_ONLY)") %}
    {% endfor %}
    {% set db_aliases = run_query("SELECT database_name FROM duckdb_databases() WHERE database_name LIKE 'daily_%'").columns[0].values() %}
{% else %}
    {% set db_aliases = [] %}
{% endif %}

with unioned_data as (
    {% for alias in db_aliases %}
        select * from "{{ alias }}".main.spain_news_monitor
        {% if not loop.last %} union all {% endif %}
    {% endfor %}
)

select 
    md5(link) as news_id,
    *,
    current_timestamp as processed_at
from unioned_data

{% if is_incremental() %}
    -- 🚀 THE KEY: Only pull news newer than what's already in news_report.duckdb
    where published > (select max(published) from {{ this }})
{% endif %}




-- Use the `ref` function to select from other models

-------select *
-------from {{ ref('my_first_dbt_model') }}
-------where id = 1
