import requests
from bs4 import BeautifulSoup
from gemeaux import Handler

from Sites import Article
import config
from TemplateStrResponse import TemplateStrResponse


BASE = "https://www.bbc.co.uk"

def get_articles():
	feeds = [
	    "http://feeds.bbci.co.uk/news/rss.xml"
	]

	article_urls = set()

	for feed in feeds:
		data = requests.get(feed)

		if data.status_code != 200:
			return None

		content = data.content.decode()

		soup = BeautifulSoup(content, features="xml")

		all_articles = soup.find_all("item")

		for a in all_articles:
			href = a.find("link").text
			title = a.find("title").text

			article_urls.add((href, title))

	articles = [Article.Article("The BBC", x[0], None, x[1], None) for x in article_urls if "/sport/" not in x[0]]

	return articles

def get_article(url):
        data = requests.get(url)

        if data.status_code != 200:
            return None

        content = data.content.decode()

        soup = BeautifulSoup(content, features="lxml")

        author = "The BBC"
        title = soup.find("h1", {"id": "main-heading"}).text.strip()

        paragraphs = soup.find_all("div", {"data-component": "text-block"})

        body = "\n\n".join(x.text for x in paragraphs)

        return Article.Article("The BBC", url, author, title, body)



def gemini_home():
	out = "# All BBC Articles:\n\n"

	articles = get_articles()

	for a in articles:
		out += "=> {} {}\n\n".format(
			a.url.replace(BASE, "/bbc"),
			a.title
		)

	return out

def gemini_article(base_url):
	url = base_url.replace("/bbc", "", 1)

	article = get_article(BASE+url)
	return f"""\
# {article.title}
## {article.author}

{article.body}

Mirrored from {BASE}{url}
"""

def http_home():
	out = "<h1>All BBC Articles:</h1><br>"

	articles = get_articles()

	for a in articles:
		out += "<a href=\"{}\">{}</a><br>".format(
			a.url.replace(BASE, "/bbc"),
			a.title
		)
		
	return out
		
def http_article(base_url):
	url = base_url.replace("/bbc", "", 1)
	print(url)

	article = get_article(BASE+url)
	return f"""\
<h1>{article.title}</h1>
<h1>{article.author}</h1>

<p>{article.body}</p>

Mirrored from <a href="{BASE}{url}">{BASE}{url}</a>
"""

