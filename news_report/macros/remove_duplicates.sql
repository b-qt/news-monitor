{% macro remove_duplicates(partition_cols, order_by_col) %}

/* {{ dbt_utils.deduplicate(
    relation=relation_to_clean,      
    partition_by=partition_cols,    
    order_by=order_by_col            
) 
}} */

qualify row_number() over (               /* qualify -- filter these results over a window by count --row_number */
        partition by {{ partition_cols }} /* partition by -- group the rows by the specified columns */
        order by {{ order_by_col }}       /* order by -- order the rows within each partition */
    ) = 1                                 /* keep only the first row in each partition */

{% endmacro %}