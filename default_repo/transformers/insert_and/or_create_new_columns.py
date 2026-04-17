if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from transformers import pipeline

import pandas as pd

import torch

import builtins
builtins.torch = torch

@transformer
def transform(data, *args, **kwargs):
    """
    This code creates columns for sentiment_labels and sentiment_scores
    """
    pipeline_sentiment_es = pipeline("sentiment-analysis", 
                                     model="pysentimiento/robertuito-sentiment-analysis",
                                     framework="pt")
    
    # SENTIMENT ANALYSIS
    print("Analyzing sentiment (English and Spanish)...")
    print(f"Columns ... {data.columns}")
    
    # Run Spanish sentiment on original (cleaned) titles
    sent_es_results = pipeline_sentiment_es(data["title"].tolist(), truncation=True)
    
    # Map results for Spanish model (Robertuito)
    label_map = {'POS': 'Positive', 'NEU': 'Neutral', 'NEG': 'Negative'}
    data['sentiment_label'] = [label_map.get(s['label'], s['label']) for s in sent_es_results]
    data['sentiment_score'] = [s['score'] for s in sent_es_results]

    print(f"New columns ... {data.columns}")
    return data 


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, pd.DataFrame),  "The output is not a dataframe; fix it!!"
    assert len(output.columns) == 7 , "The output lacks the new columns"
    
    nuevas_columnas = ['sentiment_label', 'sentiment_score']
    for col in nuevas_columnas:
        assert col in output.columns, f"¡Falta la columna {col}!"

