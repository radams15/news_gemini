from functools import reduce

import requests
from bs4 import BeautifulSoup
from gemeaux import Handler

from Sites import Article
import config
from TemplateStrResponse import TemplateStrResponse


BASE = "https://www.thetimes.co.uk"
    
def get_articles():
	data = requests.get(f"{BASE}")

	if data.status_code != 200:
		return None

	content = data.content.decode()

	soup = BeautifulSoup(content, features="lxml")

	headlines = soup.find_all("div", {"class":"Item-content"})

	article_urls = set()

	for hl in headlines:
		titles = list(hl.strings)

		title = "Unknown"

		title = " | ".join(titles)
		title = title.replace(" | Read the full story", "")
		title = title.title()
            
		if "play now" in title.lower():
			continue
            
		try:
			href = hl.find("a", {"class": "js-tracking"}).attrs["href"]

			if not BASE in href:
				href = BASE + href

		except:
			continue

		article_urls.add((href, title))

	articles = [Article.Article("The Telegraph", x[0], None, x[1], None) for x in article_urls]

	return articles

def get_article(url):
	data = requests.get(url, headers={
		"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
		"X-Forwarded-For": "66.249.66.1",
		"Cookie": ""
	})

	if data.status_code != 200:
		return None

	content = data.content.decode()

	soup = BeautifulSoup(content, features="lxml")

	main = soup.find("main", {"role": "main"})
	strings = list(map(str.strip, main.strings))

	title, author, content = strings[0], strings[1], strings[1:]

	content = "\n\n".join(content)

	return Article.Article("The Times", url, author, title, content)


def gemini_home():
	out = "# All Times Articles:\n\n"

	articles = get_articles()

	for a in articles:
		out += "=> {} {}\n\n".format(
		a.url.replace(BASE, "/times"),
		a.title
	)
	
	return out

def gemini_article(base_url):
	url = base_url.replace("/times", "", 1)

	article = get_article(BASE+url)
	return f"""\
# {article.title}
## {article.author}

{article.body}

Mirrored from {BASE}{url}
"""
