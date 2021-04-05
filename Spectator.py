import requests
from bs4 import BeautifulSoup
from gemeaux import Handler

from Article import Article
import config
from TemplateStrResponse import TemplateStrResponse


class Spectator:
    BASE = "https://www.spectator.co.uk"

    def __init__(self):
        pass

    def get_articles(self):
        data = requests.get(f"{self.BASE}/coffee-house")

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

                url = "{}{}".format(self.BASE, href)

                article_urls.add((url, title))

        articles = [Article("The Spectator", x[0], None, x[1], None) for x in article_urls]

        return articles

    def get_article(self, url):
        data = requests.get(url)

        if data.status_code != 200:
            return None

        content = data.content.decode()

        soup = BeautifulSoup(content, features="lxml")

        author = soup.find("h2", {"class": "ContentPageAuthor-module__author__name"}).text.strip()
        title = soup.find("h1", {"class": "ContentPageTitle-module__headline"}).text.strip()

        paragraphs = soup.find_all("p", {"class": "ContentPageBodyParagraph-module__paragraph--block"})

        body = "\n\n".join(x.text for x in paragraphs)

        return Article("The Spectator", url, author, title, body)

class SpectatorHandler(Handler):
    def __init__(self, *args):
        Handler.__init__(self, *args)

        self.spectator = Spectator()

    def get_response(self, url, path):
        if path == "/spectator":
            return self.home()
        else:
            return self.article(path)

    def home(self):
        out = "# All Spectator Articles:\n\n"

        articles = self.spectator.get_articles()

        for a in articles:
            out += "=> {} {}\n\n".format(
                a.url.replace(self.spectator.BASE, "gemini://{}/spectator".format(config.IP)),
                a.title
            )

        return TemplateStrResponse(out)

    def article(self, base_url):
        url = base_url.replace("/spectator", "", 1)

        article = self.spectator.get_article(self.spectator.BASE+url)
        return TemplateStrResponse(f"""\
# {article.title}
## {article.author}

{article.body}

Mirrored from {self.spectator.BASE}{url}
""")