import socket


def receive(sock: socket.socket):
    return sock.recv(4026).decode('utf-8')


def initSock(address: str, port: int):
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SOCK.connect((address, port))
    return SOCK
