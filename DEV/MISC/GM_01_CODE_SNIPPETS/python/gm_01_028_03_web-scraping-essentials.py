# PATTERN: Web Scraping Essentials

import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
# The 'soup' object now contains the parsed HTML

# PATTERN: Web Scraping Essentials

import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the first div with class 'quote'
first_quote_div = soup.find('div', class_='quote')

# Find all small tags with class 'author'
all_author_spans = soup.find_all('small', class_='author')

# PATTERN: Web Scraping Essentials

import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Select all quote texts within div.quote elements
all_quote_texts = soup.select('div.quote span.text')

# Select all tag links within div.tags
all_tag_links = soup.select('div.quote div.tags a.tag')

# PATTERN: Web Scraping Essentials

import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the first quote text span
first_quote_span = soup.find('span', class_='text')
quote_content = first_quote_span.get_text(strip=True)

# Find the first tag link
first_tag_link = soup.find('a', class_='tag')
tag_url = first_tag_link.get('href')
tag_name = first_tag_link.text