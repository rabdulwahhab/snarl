# https://www.journaldev.com/15906/python-socket-programming-server-client#python-socket-client
import socket


def server_program():
    # get the hostname
    host = "localhost"
    port = 8000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(5)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode('utf-8')
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        #data = input(' -> ')
        data = "SERVER: " + data
        conn.send(data.encode('utf-8'))  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()

