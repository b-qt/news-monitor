-- The records shouldn't have duplicate values in the title and published columns
-- Therefore return records where the count of such duplicates is greater than 1
with duplicates as (
    select 
        link,
        published,
        count(*) as duplicate_count
    from {{ ref('stg_news_incremental') }}
    group by link, published
)
select * from duplicates 
where duplicate_count > 1