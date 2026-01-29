/* Cleaned news data model */
{{ config(materialized='ephemeral') }}
/*
  This ephemeral model cleans and standardizes the news data.
  It can be referenced by other models without creating a separate table or view.
*/

with incremental_data as (

    select *
    from {{ ref('stg_news_incremental') }}

)

select 
    md5(link) as news_id,
    trim(title) as title,
    lower(source) as source,
    link,
    sentiment_label,
    sentiment_score,
    published,
    entry_date,
    --- add a flag for news from the last 24 hours
    case 
        when published >= current_timestamp - interval '24 hours' then true
        else false
    end as is_recent
from incremental_data
where link is not null
and trim(link) != ''
and link != 'None'