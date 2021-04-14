from sys import argv

import Server
import config

from Times import Times

if __name__ == "__main__":
	"""argv.append("--ip")
	#argv.append(config.IP)
	argv.append("0.0.0.0")

	server = Server.Server()
	server.serve()"""

	t = Times()

	#ats = t.get_articles()
	
	a = t.get_article("https://www.thetimes.co.uk/article/officer-denies-singing-billy-boys-anthem-0tqjz3xtm")
	
	print(a)
