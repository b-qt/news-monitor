{{
    config(
        materialized='incremental',
        unique_key='link'
    )
}}

{# 1. Find the files #}
{% set find_files_query %}
    SELECT file FROM glob('/home/src/data/*.duckdb')
    WHERE file NOT LIKE '%news_report.duckdb'
{% endset %}

{% set results = run_query(find_files_query) %}

{% if execute %}
    {% set db_files = results.columns[0].values() %}
    
    {# 2. Get currently attached databases {path: name} #}
    {% set attached_info = run_query("SELECT path, database_name FROM duckdb_databases()") %}
    {% set attached_map = {} %}
    {% for row in attached_info %}
        {% do attached_map.update({row[0]: row[1]}) %}
    {% endfor %}

    {# 3. Attach if missing, and store the REAL alias #}
    {% set final_aliases = [] %}
    {% for file in db_files %}
        {% if file in attached_map %}
            {# If already there, use the name DuckDB already gave it #}
            {% do final_aliases.append(attached_map[file]) %}
        {% else %}
            {# If not there, attach it with a clean safe name #}
            {% set new_alias = "news_archive_" ~ loop.index0 %}
            {% do run_query("ATTACH '" ~ file ~ "' AS " ~ new_alias ~ " (READ_ONLY)") %}
            {% do final_aliases.append(new_alias) %}
        {% endif %}
    {% endfor %}
{% else %}
    {% set final_aliases = [] %}
{% endif %}

with all_unioned_data as (
    {% if final_aliases | length > 0 %}
        {% for alias in final_aliases %}
            select 
                md5(link) as news_id,
                trim(title) as title,
                link,
                sentiment_label,
                cast(sentiment_score as float) as sentiment_score,
                lower(source) as source,
                cast(published as timestamp) as published,
                cast(entry_date as timestamp) as entry_date
            from "{{ alias }}".main.spain_news_monitor
            where link is not null
            and trim(link) != ''
            and lower(link) != 'none'
            and lower(link) != 'nan'
            {% if not loop.last %} union all {% endif %}
        {% endfor %}
    {% else %}
        {# Fallback if no files found yet #}
        select 
            null::text as news_id,
            null::text as title, 
            null::text as link, 
            null::text as sentiment_label, 
            null::float as sentiment_score, 
            null::text as source, 
            null::timestamp as published, 
            null::timestamp as entry_date
        limit 0
    {% endif %}
)

select * from all_unioned_data
    where link is not null
    and trim(link) != ''
    and lower(link) != 'none' 

-- Remove duplicates based on link, keeping the most recent published date
{% set partition_cols = "link" %}
{% set order_by_col = "published desc" %}
{{ remove_duplicates(partition_cols, order_by_col) }}

{% if is_incremental() %}
    -- Filter to only include rows newer than the latest date in the existing table
    and published > (select coalesce(max(published), '1900-01-01'::timestamp) from {{ this }})
{% endif %}

--- To run this in dbt, use : dbt run --select stg_news_incremental