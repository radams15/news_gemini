import requests
from bs4 import BeautifulSoup
from gemeaux import Handler

from Article import Article
import config
from TemplateStrResponse import TemplateStrResponse


class BBC:
    BASE = "https://www.bbc.co.uk"

    def __init__(self):
        pass

    def get_articles(self):
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

        articles = [Article("The BBC", x[0], None, x[1], None) for x in article_urls if "/sport/" not in x[0]]

        return articles

    def get_article(self, url):
        data = requests.get(url)

        if data.status_code != 200:
            return None

        content = data.content.decode()

        soup = BeautifulSoup(content, features="lxml")

        author = "The BBC"
        title = soup.find("h1", {"id": "main-heading"}).text.strip()

        paragraphs = soup.find_all("div", {"data-component": "text-block"})

        body = "\n\n".join(x.text for x in paragraphs)

        return Article("The BBC", url, author, title, body)

class BBCHandler(Handler):
    def __init__(self, *args):
        Handler.__init__(self, *args)

        self.bbc = BBC()

    def get_response(self, url, path):
        if path == "/bbc":
            return self.home()
        else:
            return self.article(path)

    def home(self):
        out = "# All BBC Articles:\n\n"

        articles = self.bbc.get_articles()

        for a in articles:
            out += "=> {} {}\n\n".format(
                a.url.replace(self.bbc.BASE, "/bbc"),
                a.title
            )

        return TemplateStrResponse(out)

    def article(self, base_url):
        url = base_url.replace("/bbc", "", 1)

        article = self.bbc.get_article(self.bbc.BASE+url)
        return TemplateStrResponse(f"""\
# {article.title}
## {article.author}

{article.body}

Mirrored from {self.bbc.BASE}{url}
""")
