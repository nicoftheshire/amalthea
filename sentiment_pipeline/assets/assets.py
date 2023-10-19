import json
from collection import news
from sentiment_analyzer import analyzer
from parquet import base

from dagster import AssetExecutionContext, JsonMetadataValue, asset

@asset
def collect_data(context: AssetExecutionContext):
    with open('./collection/.config.json') as config_file:
        api_keys = json.load(config_file)['news_api_keys']

    query = "USD OR dollar" # Input one query at a time so that we can tag articles properly for later sprints we can change this
    articles = news.get_news(api_keys, query)
    articles = [articles]
    if not articles:
        print("All free API requests have been depleted.")
        return

    news.save_to_json('collect_data.json', articles)

    with open("collect_data.json", "r") as f:
        metadata = {
            "preview": JsonMetadataValue(json.load(f)),
        }
        
    context.add_output_metadata(metadata=metadata)

@asset(deps=[collect_data])
def analyze_data(context: AssetExecutionContext):
    analyzer.analyze_sentiment()
    
    with open("analyze_data.json", "r") as f:
        metadata = {
            "preview": JsonMetadataValue(json.load(f)),
        }

    context.add_output_metadata(metadata=metadata)

@asset(deps=[analyze_data])
def store(context: AssetExecutionContext):
    base.store_parquet()
