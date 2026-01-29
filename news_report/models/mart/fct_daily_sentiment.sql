/*
 Marts hold the business logic of the data warehouse
 and are typically the final tables that end users will query from.
 This is where we create fact and dimension tables. 
*/
{{ config(materialized='table') }}
/*
    A 'table' is used here as this is a fact table
    which will be queried often and performance is important. 
 */

with news as (

    select *
    from {{ ref('spain_news_snapshot') }}
)
select
    --- format date to human-readable version
    {{ format_date('published') }} as date_display, -- cast(published as date) as news_date,
    sentiment_label as sentiment,
    count(*) as number_of_articles,
    round(avg(sentiment_score), 4) as avg_sentiment_confidence,
    -- most frequent source for this group
    mode(source) as top_source
from news
-- filter for the last 1 day and today
where cast(published as date) >= current_timestamp - interval '7 days'
group by 1, 2-- group by news_date, sentiment_label
order by 1 desc, 3 desc

/* Use ref() in the model definition (mart phase) */