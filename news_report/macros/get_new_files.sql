/* Macro to get new files from the data directory */
{% macro get_new_files() %}

  {# Use python glob via jinja templating to find all the duckdb files in the folder #}
  
  {% set files = modules.glob.glob('../data/*.duckdb') %}
  
  {{ return(files) }}
{% endmacro %}