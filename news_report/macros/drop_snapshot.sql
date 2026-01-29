{% macro drop_spain_snapshot() %}
    {% set query %}
        DROP TABLE IF EXISTS spain_snapshot.spain_news_snapshot
    {% endset %}
    {% do run_query(query) %}
    {{ log("Successfully dropped the snapshot table", info=True) }}
{% endmacro %}