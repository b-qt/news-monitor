-- This test asserts that the specified column in the given table does not contain any NULL values.
{% test assert_column_not_null(model, column_name) %}
  
  select *
  from {{ model }}                                 -- Reference the model (table/view) being tested
  where {{ column_name }} is null                  -- Check for NULL values
  or trim(cast({{ column_name }} as varchar)) = '' -- Also check for empty strings if the column is text-based

{% endtest %}