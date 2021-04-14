from functools import reduce

import requests
from bs4 import BeautifulSoup
from gemeaux import Handler

from Article import Article
import config
from TemplateStrResponse import TemplateStrResponse


class Times:
    BASE = "https://www.thetimes.co.uk"

    def __init__(self):
        pass

    def get_articles(self):
        data = requests.get(f"{self.BASE}")

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

                if not self.BASE in href:
                    href = self.BASE + href

            except:
                continue

            article_urls.add((href, title))

        articles = [Article("The Telegraph", x[0], None, x[1], None) for x in article_urls]

        return articles

    def get_article(self, url):
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
        strings = list(main.strings)

        print(strings)

class TimesHandler(Handler):
    def __init__(self, *args):
        Handler.__init__(self, *args)

        self.telegraph = Telegraph()

    def get_response(self, url, path):
        if path == "/telegraph":
            return self.home()
        else:
            return self.article(path)

    def home(self):
        out = "# All Times Articles:\n\n"

        articles = self.telegraph.get_articles()

        for a in articles:
            out += "=> {} {}\n\n".format(
                a.url.replace(self.telegraph.BASE, "/times"),
                a.title
            )

        return TemplateStrResponse(out)

    def article(self, base_url):
        url = base_url.replace("/times", "", 1)

        article = self.telegraph.get_article(self.telegraph.BASE+url)
        return TemplateStrResponse(f"""\
# {article.title}
## {article.author}

{article.body}

Mirrored from {self.telegraph.BASE}{url}
""")
