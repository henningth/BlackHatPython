#!/usr/bin/env python3
"""
TCP Proxy example based on Black Hat Python by Justin Seitz.

Starts a TCP proxy server, which listens for incoming 
connections. When client connects, the proxy receives data 
from the client and forwards it to the remote host (e.g. FTP server).
Likewise, when remote host sends data to proxy, the proxy 
forwards it to the client.

Command line usage:
./tcpproxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]

Non-threaded version

Henning Thomsen
"""

import socket
import sys

def receive_data(remote_socket):
    """
    Receives data from remote socket.
    Assumes remote_socket is a data 
    socket, not a listening socket.
    """

    remote_socket.settimeout(15)

    data = b""
    datalen = 4096

    while True:

        received_data = remote_socket.recv(datalen)

        data = data + received_data

        if len(received_data) < datalen:            

            break

    return data

def client_handler(client_socket, remote_host, remote_port, receive_first):
    """
    Processes client when it connects to proxy.
    """
    # Connects to remote host using a TCP socket
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to: %s:%i" % (remote_host, remote_port))

    remote_socket.connect((remote_host, remote_port))

    # Receive data from either local or remote host (via client_socket)
    if receive_first:

        data = receive_data(remote_socket)

        # Send data to localhost
        if data:

            client_socket.send(data)

    while True:
        """
        Here we do these steps in turn:
        1: Receive data from local_host
        2: Send received data in step 1 to remote_host
        3: Receive data from remote_host
        4: Send received data in step 3 to local_host
        """

        # 1: Receive data from local_host
        local_data = receive_data(client_socket)
        print("1: Receive data from local_host")

        if len(local_data) > 0: # Data was received

            # 2: Send received data in step 1 to remote_host
            remote_socket.send(local_data)
            print("2: Send received data in step 1 to remote_host")

        # 3: Receive data from remote_host
        remote_data = receive_data(remote_socket)
        print("3: Receive data from remote_host")

        if len(remote_data) > 0:

            # 4: Send received data in step 3 to local_host
            client_socket.send(remote_data)
            print("4: Send received data in step 3 to local_host")

        if len(local_data) == 0 or len(remote_data) == 0:
            print("No more data to exchange, closing connections.")
            client_socket.close()
            remote_socket.close()
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    """
    Starts the listening server.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_host, local_port))
    print("Listening on %s:%i" % (local_host, local_port))
    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Received incoming connection from: %s:%i" % (local_host, local_port))

        # Start client
        client_handler(client_socket, remote_host, remote_port, receive_first)

def main():
    """
    Main entry point of program
    """

    if len(sys.argv) != 6:
        print("Usage: ./tcpproxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("For example: ")
        print("./tcpproxy.py 127.0.0.1 8000 website.com 80 False")

    else:

        # Set local host and port
        local_host = sys.argv[1]
        local_port = int(sys.argv[2])

        # Set remote host
        remote_host = sys.argv[3]
        remote_port = int(sys.argv[4])

        if sys.argv[5] == "True":
            receive_first = True
        else:
            receive_first = False

        # Starts the proxy server
        server_loop(local_host, local_port, remote_host, remote_port, receive_first)

main()