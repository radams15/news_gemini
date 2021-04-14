from gemeaux import App, Handler

from Sites import BBC
from Sites import Spectator
from Sites import Telegraph
from Sites import Times

from TemplateStrResponse import TemplateStrResponse


class HomeHandler(Handler):
    def __init__(self, *args):
        Handler.__init__(self, *args)
        
    def home(self):
        return TemplateStrResponse(f"""\
# Rhys' News Hosting
## Here are my sites:

=> /spectator The Spectator
=> /telegraph The Telegraph
=> /bbc The BBC
=> /times The Times
""")

    def get_response(self, url, path):
    	if path == "/":
    		return self.home()
    	
    	
    	if path.startswith("/spectator"):
    		if path == "/spectator":
    			return TemplateStrResponse(Spectator.gemini_home())
    		else:
    			return TemplateStrResponse(Spectator.gemini_article(path))
    			
    	elif path.startswith("/telegraph"):
    		if path == "/telegraph":
    			return TemplateStrResponse(Telegraph.gemini_home())
    		else:
    			return TemplateStrResponse(Telegraph.gemini_article(path))

    	elif path.startswith("/bbc"):
    		if path == "/bbc":
    			return TemplateStrResponse(BBC.gemini_home())
    		else:
    			return TemplateStrResponse(BBC.gemini_article(path))
    			
    	elif path.startswith("/times"):
    		if path == "/times":
    			return TemplateStrResponse(Times.gemini_home())
    		else:
    			return TemplateStrResponse(Times.gemini_article(path))


class GeminiServer:
    def __init__(self):
        pass

    def serve(self):
        urls = {
            "": HomeHandler()
        }

        app = App(urls)

        app.run()
