import requests
import json


def get_news(api_keys, query):
	"""
	Fetch news articles from the NewsAPI based on the provided query.

	Args:
		api_keys (list): List of API keys for NewsAPI.
		query (str): Query term for fetching news articles.

	Returns:
		list: List of dictionaries containing tagged news articles.
	"""
	for i in range(0, 1):
		api_key = api_keys[i]
		url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
		response = requests.get(url)
		data = response.json()

		# Adding tags to articles to categorize data
		if 'articles' in data:
			for article in data["articles"]:
				article["tag"] = query
			return data['articles']
		else:
			print(f"API key {api_key} has no available article requests. Trying the next key...")
	return []


def save_to_json(filename, articles):
	"""
	Save a list of articles to a JSON Lines file.
	
	Args:
		filename (str): Name of the JSON Lines file.
		articles (list): List of dictionaries containing articles.
	"""
	with open(filename, 'w') as f:
		for article in articles:
			line = json.dumps(article)
			f.write(line)
			f.write("\n")
		f.close()
