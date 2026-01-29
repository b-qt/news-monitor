{% macro remove_duplicates(partition_cols, order_by_col) %}

qualify row_number() over (                 -- qualify filters by row number() 
        partition by {{ partition_cols }}
        order by {{ order_by_col }}
   ) = 1

{% endmacro %}