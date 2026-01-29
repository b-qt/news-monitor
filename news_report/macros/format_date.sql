{% macro format_date(column_name, format_str='%d %b %Y') %}
    {#
        This macro casts the column to a TIMESTAMP (to be safe)
        and then formats it into a human-readable string.
        Default: 28 jan 2026
    #}

    strftime(cast({{ column_name }} as timestamp), '{{ format_str }}')
{% endmacro %}

/* This macro is called in
    - fct_daily_sentiment | news_date
    - spain_news_snapshot | published
   to format the date into a more readable format when displayed */