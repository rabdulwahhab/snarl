#!/usr/bin/env python3.6

import sys
import argparse
import re
import socket

sys.path.append("../")
from Util import logInFile

log = logInFile("snarlClient.py")


def main():
    try:
        ADDRESS = '127.0.0.1'
        PORT = 45678

        parser = argparse.ArgumentParser()
        parser.add_argument("--address",
                            nargs='?',
                            help="Enter the IP address to listen for connections",
                            const=ADDRESS, type=str)
        parser.add_argument("--port",
                            nargs='?',
                            help="Enter the port number to listen on",
                            const=PORT, type=int)

        args = parser.parse_args()

        # Parse options
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

        SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SOCK.connect((ADDRESS, PORT))
        print(SOCK.recv(4026).decode('utf-8'))  # Welcome message

        # TODO move to Client.py
        while True:
            resp = SOCK.recv(4026).decode('utf-8')
            print(resp)
            msg = input()
            SOCK.send(msg.encode('utf-8'))

    except BrokenPipeError:
        print("\nLost connection with the host...")
        sys.exit(1)
    except EOFError:
        print("\nQuitting...")
        if SOCK:
            SOCK.shutdown()
            SOCK.close()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(1)


if __name__ == '__main__':
    main()
