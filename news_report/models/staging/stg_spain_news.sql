/* Staging model for Spain news data
   In here we do "light cleaning" which involves
   removing duplicates and standardizing data formats */

{{ config(materialized='view') }} 
/*
  A 'view' is used here to save storage space as this is 
  a staging table and can be easily recomputed as needed.  
  
  If performance becomes an issue, consider changing to 'table'
  because tables are faster to query than views.
*/

with raw_data as (

    select *
    from {{ ref('stg_news_incremental') }} -- source(table_name, source_name)

)
select
    -- 1. Create a news_id using a hash of the link (Best practice!)
    md5(link) as news_id,
    title,
    link,
    sentiment_label,
    sentiment_score,
    source,
    published,
    entry_date
from raw_data
-- 2. FIX: Change 'id' to 'link' or 'title'
where link is not null

/* Use source() in the model definition (staging phase) */