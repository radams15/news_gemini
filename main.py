from sys import argv

import Server
import config

if __name__ == "__main__":
    argv.append("--ip")
    argv.append(config.IP)

    server = Server.Server()
    server.serve()
