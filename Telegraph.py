from functools import reduce

import requests
from bs4 import BeautifulSoup
from gemeaux import Handler

from Article import Article
import config
from TemplateStrResponse import TemplateStrResponse


class Telegraph:
    BASE = "https://www.telegraph.co.uk"

    def __init__(self):
        pass

    def get_articles(self):
        data = requests.get(f"{self.BASE}")

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

                if not self.BASE in href:
                    href = self.BASE + href
            except:
                continue

            article_urls.add((href, title))

        articles = [Article("The Spectator", x[0], None, x[1], None) for x in article_urls]

        return articles

    def get_article(self, url):
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

        return Article("The Spectator", url, author, title, body)

class TelegraphHandler(Handler):
    def __init__(self, *args):
        Handler.__init__(self, *args)

        self.telegraph = Telegraph()

    def get_response(self, url, path):
        if path == "/telegraph":
            return self.home()
        else:
            return self.article(path)

    def home(self):
        out = "# All Spectator Articles:\n\n"

        articles = self.telegraph.get_articles()

        for a in articles:
            out += "=> {} {}\n\n".format(
                a.url.replace(self.telegraph.BASE, "gemini://{}/telegraph".format(config.IP)),
                a.title
            )

        return TemplateStrResponse(out)

    def article(self, base_url):
        url = base_url.replace("/telegraph", "", 1)

        article = self.telegraph.get_article(self.telegraph.BASE+url)
        return TemplateStrResponse(f"""\
# {article.title}
## {article.author}

{article.body}

Mirrored from {self.telegraph.BASE}{url}
""")