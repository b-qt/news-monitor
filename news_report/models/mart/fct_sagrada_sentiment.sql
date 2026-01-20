/* This model aggregates sentiment data for Sagrada Familia mentions in news articles. */
{{ config(materialized='table') }}
with news as (

    select *
    from {{ ref('ephemeral_spain_news') }}

)
/* select distinct(*) from news
where title ilike '%sagrada%'
order by published desc */

select 
    -- 1. These are your "Buckets" (Dimensions)
    cast(published as date) as news_date,
    sentiment_label,
    source,
    title,

    -- 2. These are your "Metrics" (Aggregates)
    count(*) as article_count,
    --round(avg(sentiment_score), 4) as avg_sentiment_confidence

from news
where title ilike '%sagrada%'

-- 3. FIX: You must list columns 1, 2, and 3 here
group by 1, 2, 3, 4
-- (Or group by news_date, sentiment_label, source)

order by news_date desc