from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor 
from concurrent import futures

def fetch_full_article_content(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None  # Failed to get a successful response
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Assume the article content is within <p> tags
        paragraphs = soup.find_all('p')
        
        # Join all paragraph texts
        full_content = ' '.join([p.text for p in paragraphs])
        
        return full_content
    except Exception as e:
        print(f"Failed to fetch full article content: {e}")
        return None

def fetch_content_concurrently(article_data_list):
    fetched_contents = []
    with ThreadPoolExecutor(max_workers=10) as executor: 
        future_to_url = {executor.submit(fetch_full_article_content, article['url']): article for article in article_data_list}
        for future in futures.as_completed(future_to_url):
            article = future_to_url[future]
            try:
                fetched_content = future.result()
            except Exception as e:
                print(f"An error occurred while fetching {article['url']}: {e}")
                fetched_content = None
            fetched_contents.append((article, fetched_content))
    return fetched_contents