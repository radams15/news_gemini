import requests
from bs4 import BeautifulSoup
from gemeaux import Handler

from Sites import Article
import config
from TemplateStrResponse import TemplateStrResponse


BASE = "https://www.spectator.co.uk"
    
def get_articles():
	data = requests.get(f"{BASE}/coffee-house")

	if data.status_code != 200:
		return None

	content = data.content.decode()

	soup = BeautifulSoup(content, features="lxml")

	all_articles = soup.find_all("article")

	article_urls = set()

	for a in all_articles:
		for links in a.find_all("a"):
			header = a.find("h2")

			href = links.attrs["href"]
			if "writer/" in href:
				continue

	title = header.text

	url = "{}{}".format(BASE, href)

	article_urls.add((url, title))

	articles = [Article.Article("The Spectator", x[0], None, x[1], None) for x in article_urls]

	return articles


def get_article(url):
	data = requests.get(url)

	if data.status_code != 200:
		return None

	content = data.content.decode()

	soup = BeautifulSoup(content, features="lxml")

	author = soup.find("h2", {"class": "ContentPageAuthor-module__author__name"}).text.strip()
	title = soup.find("h1", {"class": "ContentPageTitle-module__headline"}).text.strip()

	paragraphs = soup.find_all("p", {"class": "ContentPageBodyParagraph-module__paragraph--block"})

	body = "\n\n".join(x.text for x in paragraphs)

	return Article.Article("The Spectator", url, author, title, body)


def gemini_home():
	out = "# All Spectator Articles:\n\n"

	articles = get_articles()

	for a in articles:
		out += "=> {} {}\n\n".format(
		a.url.replace(BASE, "/spectator"),
		a.title
	)

	return out

def gemini_article(base_url):
	url = base_url.replace("/spectator", "", 1)

	article = get_article(BASE+url)
	return f"""\
# {article.title}
## {article.author}

{article.body}

Mirrored from {BASE}{url}
"""
