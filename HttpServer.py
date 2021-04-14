from flask import Flask

from Sites import BBC
from Sites import Spectator
from Sites import Telegraph
from Sites import Times

from TemplateStrResponse import TemplateStrResponse

app = Flask(__name__)

        
@app.route("/")
def home():
	return f"""\
# Rhys' News Hosting
## Here are my sites:

=> /spectator The Spectator
=> /telegraph The Telegraph
=> /bbc The BBC
=> /times The Times
"""

@app.route("/spectator/<path:text>", methods=["GET"])
@app.route("/spectator", methods=["GET"])
def spec(path="/spectator"):
	if path == "/spectator":
		return Spectator.gemini_home()
	else:
		return Spectator.gemini_article(path)
    	
@app.route("/telegraph/<path:text>", methods=["GET"])
@app.route("/telegraph", methods=["GET"])
def tele(path="/telegraph"):		
	if path == "/telegraph":
		return Telegraph.gemini_home()
	else:
		return Telegraph.gemini_article(path)
   
@app.route("/bbc/<path>", methods=["GET"])
@app.route("/bbc", methods=["GET"])
def bbc(path="/bbc"):
	if path == "/bbc":
		return BBC.http_home()
	else:
		return BBC.http_article(path)
    			
@app.route("/times/<path:text>", methods=["GET"])
@app.route("/times", methods=["GET"])
def times(path="/times"):
	if path == "/times":
		return Times.gemini_home()
	else:
		return Times.gemini_article(path)


class HttpServer:
    def __init__(self):
        pass

    def serve(self):
        app.run()
