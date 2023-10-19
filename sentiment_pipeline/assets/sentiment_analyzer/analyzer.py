from textblob import TextBlob
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
from web_scraper import fetch_content_concurrently
from data_cleaner import DataCleaner  # Import the DataCleaner class
import re

# Initialize Hugging Face sentiment analysis model and tokenizer
sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
sentiment_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Create an instance of DataCleaner
data_cleaner = DataCleaner()


def analyze_sentiment_with_textblob(content):
    sentences = re.split(r'[.!?]', content)
    total_score = 0
    total_sentences = 0

    for sentence in sentences:
        blob = TextBlob(sentence)
        sentiment = blob.sentiment.polarity
        score = (sentiment + 1) * 5  # Convert to a scale of 1 to 10
        total_score += score
        total_sentences += 1

    if total_sentences == 0:
        return 0
    else:
        average_score = total_score / total_sentences

    return average_score


def analyze_sentiment_with_hugging_face(content, currency_tags):
    sentences = re.split(r'[.!?]', content)
    total_score = 0
    total_sentences = 0
    for sentence in sentences:
        tokens = sentiment_tokenizer(sentence, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            output = sentiment_model(**tokens)
        probabilities = torch.softmax(output.logits, dim=1)
        positive_prob = probabilities[0][1].item()
        score = 1 + positive_prob * 9
        total_score += score
        total_sentences += 1
    if total_sentences == 0:
        return 0
    else:
        average_score = total_score / total_sentences
    return average_score


def analyze_sentiment():
    with open("collect_data.json", "r") as collect:
        data = json.load(collect)

    fetched_contents = fetch_content_concurrently(data)
    results = []

    for article_data, full_content in fetched_contents:
        if full_content:
            content = full_content
        else:
            content = article_data.get('content', '')

        if not content:
            print("Invalid article data.")
            continue

        # Initialize a 'translated' flag as False
        translated = False

        # Perform translation and cleaning
        data_cleaner = DataCleaner()
        cleaned_content, translated = data_cleaner.clean_and_translate(content)

        currency_tags = article_data.get('tag', 'Unknown')
        textblob_score = analyze_sentiment_with_textblob(cleaned_content)
        hugging_face_score = analyze_sentiment_with_hugging_face(cleaned_content, currency_tags)

        # Calculate the average score based on TextBlob and Hugging Face sentiment analysis
        average_score = (textblob_score + hugging_face_score) / 2

        if average_score >= 6:
            average_sentiment = "Positive"
        elif average_score <= 4:
            average_sentiment = "Negative"
        else:
            average_sentiment = "Neutral"

        result = {
            "hugging_face_response": hugging_face_score,
            "textblob_response": textblob_score,
            "average_response": average_score,
            "title": article_data.get('title', 'Unknown'),
            "author": article_data.get('author', 'Unknown'),
            "description": article_data.get('description', 'Unknown'),
            "url": article_data.get('url', 'Unknown'),
            "urlToImage": article_data.get('urlToImage', 'Unknown'),
            "publishedAt": article_data.get('publishedAt', 'Unknown'),
            "content": cleaned_content,
            "tag": article_data.get('tag', 'Unknown'),
            "source_id": article_data.get('source', {}).get('id', 'Unknown'),
            "source_name": article_data.get('source', {}).get('name', 'Unknown'),
            "currency": currency_tags,
            "average_sentiment": average_sentiment,
            "translated": translated
        }
        results.append(result)

    with open("analyze_data.json", 'w') as f:
        json.dump(results, f)
