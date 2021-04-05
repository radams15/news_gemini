from gemeaux import App, Handler

from BBC import BBCHandler
from Spectator import SpectatorHandler
from Telegraph import TelegraphHandler

from TemplateStrResponse import TemplateStrResponse


class HomeHandler(Handler):
    def __init__(self, *args):
        Handler.__init__(self, *args)

    def get_response(self, url, path):
        return TemplateStrResponse(f"""\
# Rhys' News Hosting
## Here are my sites:

=> /spectator The Spectator
=> /telegraph The Telegraph
=> /bbc The BBC
        """)

class Server:
    def __init__(self):
        pass

    def serve(self):
        urls = {
            "/spectator": SpectatorHandler(),
            "/telegraph": TelegraphHandler(),
            "/bbc": BBCHandler(),
            "/": HomeHandler()
        }

        app = App(urls)

        app.run()