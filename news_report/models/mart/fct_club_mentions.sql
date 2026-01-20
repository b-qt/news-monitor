/*
   This model aggregates club mentions from news articles.
*/
{{ config(materialized='table') }} -- Use 'table' materialization for performance 
with news as (

    select *
    from {{ ref('ephemeral_spain_news') }}

),
club_mentions as (
    select * from {{ ref('club_locations')}} -- Seeds are referenced using ref('...')
)
select 
    c.name,
    c.neighborhood,
    n.news_id,
    n.title,
    n.sentiment_label,
    n.sentiment_score,
    n.published
from news n
join club_mentions c
    --- Find mentions by checking if name is in the title (case insensitive)
    on lower(n.title) ilike '%' || lower(c.name) || '%'
order by n.published desc
