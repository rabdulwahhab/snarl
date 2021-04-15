#!/usr/bin/env python3.6

import sys
import argparse
import re
import Server

sys.path.append("../")
from Util import logInFile

"""
The Snarl Server:

- dish out connections
- create new game 
- handle joins 
- start game 
- administer game
    - broadcast game 
- end game
"""

log = logInFile("snarlServer.py")


def main():
    log = logInFile("Server.py")

    try:
        DEFAULT_LEVEL = './snarl.levels'
        CLIENTS = 4
        WAIT = 60
        OBSERVE = False
        ADDRESS = '127.0.0.1'
        PORT = 45678

        parser = argparse.ArgumentParser()  # initialize
        # this is how you add an optional argument
        parser.add_argument("--levels",
                            help="Enter the name of an input JSON Level file",
                            nargs='?',
                            const=DEFAULT_LEVEL, type=str)
        parser.add_argument("--clients",
                            help="Enter the amount of clients connecting to the game",
                            nargs='?',
                            const=CLIENTS, type=int)
        parser.add_argument("--wait",
                            nargs='?',
                            help="Enter the amount of time to wait for the next client to connect",
                            const=WAIT, type=int)
        parser.add_argument("--observe", help="Observe the game",
                            action="store_true")
        parser.add_argument("--address",
                            nargs='?',
                            help="Enter the IP address to listen for connections",
                            const=ADDRESS, type=str)
        parser.add_argument("--port",
                            nargs='?',
                            help="Enter the port number to listen on",
                            const=PORT, type=int)

        # this is called after you define your optional args
        args = parser.parse_args()

        # Global vars
        JSON_LEVELS = None
        NUM_LEVELS = 0

        # Parse options
        if args.levels:
            # global NUM_LEVELS, JSON_LEVELS, log
            log('got levels flag', args.levels)
            with open(args.levels) as file:
                wholeFile = file.read()
                portions = wholeFile.split('\n\n')
                cleaned = list(filter(lambda port: port != '', portions))
                NUM_LEVELS = int(cleaned[0])
                JSON_LEVELS = cleaned[1:]
        else:
            log("using default level")
            # global NUM_LEVELS, JSON_LEVELS, log
            with open(DEFAULT_LEVEL) as file:
                wholeFile = file.read()
                portions = wholeFile.split('\n\n')
                cleaned = list(filter(lambda port: port != '', portions))
                NUM_LEVELS = int(cleaned[0])
                JSON_LEVELS = cleaned[1:]

        if args.clients:
            # global CLIENTS, log
            if 1 <= args.clients <= 4:
                log('got clients flag', str(args.clients))
                CLIENTS = args.clients
            else:
                print("Clients must be from 1-4")
                sys.exit(1)

        if args.wait:
            # global WAIT, log
            log('got wait flag', str(args.wait))
            WAIT = args.wait

        if args.observe:
            # global OBSERVE, log
            log('got observe')
            OBSERVE = True

        if args.address:
            # global ADDRESS, log
            log("got address flag")
            if re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", args.address):
                ADDRESS = args.address
            else:
                print("Invalid address given. Try again")
                sys.exit(1)

        if args.port:
            # global PORT, log
            log("got port flag")
            if 2000 <= args.port <= 65000:
                log('got port flag', str(args.port))
                PORT = args.port
            else:
                print("Invalid port number. Try again")
                sys.exit(1)

        # Ready to begin
        args = {
            'port': PORT,
            'address': ADDRESS,
            'observe': OBSERVE,
            'jsonLevels': JSON_LEVELS,
            'numLevels': NUM_LEVELS,
            'wait': WAIT,
            'numClients': CLIENTS
        }

        Server.start(args)

    except FileNotFoundError:
        print("Couldn't find that level file. Try again")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(1)


if __name__ == '__main__':
    main()
