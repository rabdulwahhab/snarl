#!/usr/bin/env python3

import socket
import sys


def main():
    args = sys.argv[1:]

    if len(args) == 3:
        (hostName, port, userName) = args
    elif len(args) == 2:
        (hostName, port, userName) = [args[0], args[1],
                                      "Glorifrir Flintshoulder"]
    if len(args) == 1:
        (hostName, port, userName) = [args[0], 8000, "Glorifrir Flintshoulder"]
    else:
        (hostName, port, userName) = ["localhost", 8000,
                                      "Glorifrir Flintshoulder"]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostName, port))

    print("Listening on port %d" % port)

    while True:
        try:
            msg = input("Reading input > ")
            sock.send(msg.encode("utf-8"))
            data = sock.recv(4096).decode("utf-8")
            print(data)
        except:
            print("Connection closed.")
            exit(0)


if __name__ == '__main__':
    main()
