{{ config(materialized='ephemeral') }}
/*
  Ephemeral models do not create physical tables or views in the database.
  Instead, they are inlined into dependent models at runtime.
  This is useful for reusable logic that doesn't need to be stored separately.
*/



/* --select * from {{ ref('stg_spain_news') }} */
select * from {{ ref('int_news_cleaned') }}


/*
    This ephemeral model encapsulates the logic for daily sentiment aggregation.
    It can be referenced by other models without creating a separate table or view.

    This approach optimizes storage while maintaining modularity in the data transformation process.

    It retrns all the data from the source ... to apply transformations and aggregations, we reference
    this model in the snapshot configuration. 
 */