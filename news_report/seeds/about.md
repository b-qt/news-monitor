A seed is a file that contains initial data or content used to populate a database, application, or system. In the context of a news report application, a seed file might include predefined articles, sources, or metadata that help set up the application for testing or demonstration purposes.

The seed file is a csv file that can be referenced to populate the database, using the ref function ... it usually contains a list of mappings.
Avoid using the dbt seed to load raw data, load sensitive data.

Run the `dbt seed` command to load the seed data into your data warehouse. This command reads the seed files defined in your project and inserts the data into the corresponding tables in your database.