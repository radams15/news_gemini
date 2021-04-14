from sys import argv

import GeminiServer
import HttpServer
import config

if __name__ == "__main__":
	argv.append("--ip")
	argv.append("0.0.0.0")

	gs = GeminiServer.GeminiServer()
	gs.serve()
	
	#hs = HttpServer.HttpServer()
	#hs.serve()
