---
title: Spain News Monitor
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
---

# Pulse on the Iberian Region: Spanish newsletter monitor
> Stop reading the news, start understanding the sentiment!!

I'm building an automated pipeline that scrapes Spanish-language news headlines about Spain, assesses the "sentiment" (Positive/Negative) of the news, and reports them for general understanding of Spainish sentiment.  
__Serverless__ ... Instead of running a dedicated database server, I'm using a serverless data warehouse -_DuckDB_ for storage and _HuggingFace Inference API_ for the heavylifting. This is going to be orchestrated by _Mage_ running in _Docker_.  

### The "how" to reproduce this project
#### Steps to clone and run locally ... _Option 1_
1. Clone the repo > `git clone https://github.com/b-qt/news-monitor.git`
2. Install dependencies > `pip install -r requirements.txt`
3. Run the application > `docker-compose up --build -d`
4. Access the app in your browser at `http://localhost:8501`
#### Steps to clone and run locally ... _Option 2_
1. > `docker run -it -p 7860:7860 --platform=linux/amd64 \
	registry.hf.space/b-qt-spain-news:latest` 
<!---[![Preview of the app](preview.png)] (http://localhost:8501)--->

## The Stack
- Orchestration : Mage in Docker
- Compute/Transformations : Python|pandas
- ML & Transformations : Serverless HuggingFace Inference API
- Storage : DuckDB
- Visualization | Frontend : Looker Studio and/or streamlit

## Data source 
> _google news rss feeds_   
[Link 1](https://news.google.com/rss/search?q=Espa%C3%B1a&hl=es&gl=ES&ceid=ES%3Aes) ;  
[Link 2](https://news.google.com/rss/search?q=Spain&hl=en-US&gl=US&ceid=US%3Aen)

__Why__? free, realtime, legal to scrape via rss and allows complex filtering.  


## Machine learning component
Using models from huggingface ...  
- Translation (Spanish-to-English) | helsinki-nlp
- Sentiment Analysis | distilbert

### What is exciting about this project?
Other tha guaging the mood of the country via the news outlets ???  
- The prospect of batching when using the huggingface api _Unnecessary because of the volume of data being injested_
- RSS feed date formats _pd.to-datetime() fixes the inconsistences _
- Possibility of duplicate data so i need to implement data quality checks.
- Working with realtime data from API calls. | _Exciting_
- _Enriching_ the data with AI. _HuggingFace_
- Offloading storage and compute to the cloud, hence keeping my docker container lightweight... _DuckDb is more lightweight than a traditional database_