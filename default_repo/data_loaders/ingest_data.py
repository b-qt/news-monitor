import io
import pandas as pd
import requests
import feedparser

from datetime import datetime

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

URLS = [
    'https://news.google.com/rss/search?q=Espa%C3%B1a&hl=es&gl=ES&ceid=ES%3Aes',
    'https://news.google.com/rss/search?q=Spain&hl=en-US&gl=US&ceid=US%3Aen'
]
@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Fetches and cleans RSS data into a flat DataFrame.
    """
    all_rows = []
    now = pd.Timestamp.now()

    for url in URLS:
        print(f"Fetching: {url}") 
        feed = feedparser.parse(url)
        print(f"\t{len(feed.entries)} entries ...")
        
        for entry in feed.entries:
            row = {
                'title': entry.get('title').split("-")[0],
                'link': entry.get('link'),
                'published': pd.to_datetime(entry.get('published'), errors='coerce'),
                # Google News 'source' is a dict, we just want the name
                'source': entry.get('source', {}).get('title', 'N/A'),
                'entry_date': pd.to_datetime(now)
            }
            all_rows.append(row)

    # Create the DataFrame once at the end
    return pd.DataFrame(all_rows)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, pd.DataFrame), 'Output is not a dataframe'
