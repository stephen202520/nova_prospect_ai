# core/web_scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        texts = soup.stripped_strings
        content = ' '.join(texts)
        return content[:1000]  # Limit to 1000 characters
    except Exception as e:
        print(f"[!] Error extracting content from {url}: {e}")
        return ""