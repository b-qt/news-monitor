if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

def standardize_data(data):
    """Standardize date formats and text data."""
    for category, df in data.items():
        df['published'] = pd.to_datetime(df['published'], errors='coerce')
        df['title'] = df['title'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
    return data

from pysentimiento import create_analyzer
def perform_sentiment_analysis(data):
    """Perform sentiment analysis on the news titles using robertuito transformer"""
    analyzer = create_analyzer(task="targeted_sentiment", lang="es")
    for category, df in data.items():
        df['sentiment_label'] = df['title'].apply(lambda x: analyzer.predict(x).output)
    return data

def extract_into_multiple_dataframes(data):
    """Split the single dataframe into 3 separate dataframes which can be pushed into the warehouse"""
    data_economy = data['economy']
    data_tech = data['tech']
    data_real_estate = data['real_estate']
    return data_economy, data_tech, data_real_estate
    
def merge_dataframes(data_economy, data_tech, data_real_estate):
    """Merge the three category-specific DataFrames into a single DataFrame with an additional 'category' column."""
    data_economy['category'] = 'economy'
    data_tech['category'] = 'tech'
    data_real_estate['category'] = 'real_estate'
    
    merged_df = pd.concat([data_economy, data_tech, data_real_estate], ignore_index=True)
    return merged_df

@transformer
def transform(data, *args, **kwargs):
    """
    Currently we have a dictionary of DataFrames for economy, tech and real estate news. 
    In this transformer, we are preparing the data for storage in the warehouse. Necessary transformations include:
    - Standardizing date formats
    - Performing sentiment analysis on the news titles to create a new 'sentiment_label' column
    - Extracting keywords from the titles and creating a new 'keywords' column for future analysis.
    - Ensuring that all text data is in a consistent format (e.g., lowercase, removing special characters) to facilitate future analysis.
    """
    standardized_data = standardize_data(data)
    sentimental_data = perform_sentiment_analysis(standardized_data)
    data_economy, data_tech, data_real_estate = extract_into_multiple_dataframes(sentimental_data)

    data = merge_dataframes(data_economy, data_tech, data_real_estate)
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
