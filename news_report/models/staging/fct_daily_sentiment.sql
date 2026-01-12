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
    from {{ ref('stg_spain_news') }}

)
select 
    cast(published as date) as news_date,
    sentiment_label,
    count(*) as article_count,
    round(avg(sentiment_score), 4) as avg_sentiment_confidence,
    mode(source) as top_source
from news
group by 1,2 -- group by news_date, sentiment_label
order by 1 desc