from functools import reduce

import requests
from bs4 import BeautifulSoup
from gemeaux import Handler

from Sites import Article
import config
from TemplateStrResponse import TemplateStrResponse


BASE = "https://www.telegraph.co.uk"

def get_articles():
	data = requests.get(f"{BASE}")

	if data.status_code != 200:
		return None

	content = data.content.decode()

	soup = BeautifulSoup(content, features="lxml")

	headlines = soup.find_all("h3", {"class":"list-headline"})

	article_urls = set()

	for hl in headlines:
		titles = list(hl.strings)

		title = "Unknown"

		for t in titles:
			if t.strip(): title = t.strip()

		try:
			href = hl.find("a", {"class": "list-headline__link"}).attrs["href"]

			if not BASE in href:
				href = BASE + href
		except:
			continue

		article_urls.add((href, title))

	articles = [Article.Article("The Telegraph", x[0], None, x[1], None) for x in article_urls]

	return articles

def get_article(url):
	data = requests.get(url)

	if data.status_code != 200:
		return None

	content = data.content.decode()

	soup = BeautifulSoup(content, features="lxml")

	author = soup.find("span", {"class": "e-byline__author"}).text.strip()
	title = soup.find("h1", {"class": "e-headline"}).text.strip()

	bodies = soup.find_all("div", {"class": "article-body-text"})
	paragraphs = reduce(lambda z, y :z + y, [x.find_all("p") for x in bodies])

	body = "\n\n".join(x.text for x in paragraphs)

	return Article.Article("The Telegraph", url, author, title, body)


def gemini_home():
	out = "# All Telegraph Articles:\n\n"

	articles = get_articles()

	for a in articles:
	    out += "=> {} {}\n\n".format(
		a.url.replace(BASE, "/telegraph"),
		a.title
	    )

	return out

def gemini_article(base_url):
	url = base_url.replace("/telegraph", "", 1)

	article = get_article(BASE+url)
	return f"""\
# {article.title}
## {article.author}

{article.body}

Mirrored from {BASE}{url}
"""



