if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader 
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import feedparser  
import pandas as pd  

@data_loader
def load_data(*args, **kwargs):
    """
    Load the data from google rss feed for Spain. 
    The url endpoints point to economy, tech and real estate news respectively. 
    
    The result is a dictionary with three keys: 'economy', 'tech' and 'real_estate'. Each key contains a DataFrame with the corresponding news articles.
    """
    
    # Define the RSS feed URLs for economy, tech, and real estate news in Spain
    rss_feeds = {
        'economy': 'https://news.google.com/rss/search?q=econom%C3%ADa+site:es&hl=es&gl=ES&ceid=ES:es',
        'tech': 'https://news.google.com/rss/search?q=tecnolog%C3%ADa+site:es&hl=es&gl=ES&ceid=ES:es',
        'real_estate': 'https://news.google.com/rss/search?q=inmobiliaria+site:es&hl=es&gl=ES&ceid=ES:es'
    }
    
    data = {}
    
    for category, url in rss_feeds.items():
        feed = feedparser.parse(url)
        articles = []
        
        for entry in feed.entries:
            #print(entry.keys())
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': pd.to_datetime(entry.published, errors='coerce').date() if 'published' in entry else pd.NaT,
                'source': entry.source.title if 'source' in entry else 'Unknown',
                'entry_date':pd.to_datetime("today").date()
            })
        
        data[category] = pd.DataFrame(articles)
    
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert output['economy'].shape[0] > 0, 'No economy news articles were loaded'
    assert output['tech'].shape[0] > 0, 'No tech news articles were loaded'
    assert output['real_estate'].shape[0] > 0, 'No real estate news articles were loaded'
