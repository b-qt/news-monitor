/* This model aggregates sentiment data for Sagrada Familia mentions in news articles. */
{{ config(materialized='table') }}
with news as (

    select *
    from {{ ref('sagrada_sentiment_snapshot') }}

)
select 
    -- 1. These are "Buckets" (Dimensions)
    cast(published as date) as news_date,
    sentiment_label,
    source,
    title,

    -- 2. These are "Metrics" (Aggregates)
    count(*) as article_count,
    round(avg(sentiment_score), 4) as avg_sentiment_confidence

from news
group by 1, 2, 3,4
-- (Or group by news_date, sentiment_label, source, title)
order by news_date desc