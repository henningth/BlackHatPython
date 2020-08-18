#!/usr/bin/env python3
"""

Netcat replacement written in Python.
Based on bhnet.py in the book Black Hat Python 
by Justin Seitz.

Henning Thomsen

This program can run as client or server

Server features:

(1): Listens on specified TCP port for incoming client requests

Client features:

(1): Connects to server (ncpython), which returns a command shell
(2): Connects to server (ncpython) and uploads file

"""

# Standard library imports
import socket as skt
import sys
import threading

# Third party imports
import getopt

# Global variables
target = ""
port = 0
listen = False

def usage():
    """
    Prints usage
    """
    print("Netcat-inspired implementation in Python.")
    print("Usage: ./ncpython.py -t target -p port <commands>")
    print("Here <commands can be be one of:>")
    print("-l: listen for incoming connections (server mode)")
    print("-u <filename>: upload file to remote server (client mode)")
    print("-c: return a command shell (client mode)")
    print("-h: prints usage (both client, server)")

def client():
    """
    This is called when program is in client mode
    """
    pass

def client_handler():
    """
    Client handling process, spawned when client 
    connects to listening server
    """
    pass

def server():
    """
    Main server function, is started if user 
    wants program to listen on a port
    """

    # Creates listening socket
    server_socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

    server_socket.bind((target, port))

    server_socket.listen(5)

    # Each time client connects, spawn thread
    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))

        client_thread.start()

def main():
    """
    Main entry point of program
    """
    global target
    global port
    global listen

    # Parse commandline options
    options, arguments = getopt.getopt(sys.argv[1:], "ht:p:lu:c",
                                                     ["help", "target", "port", "listen", "upload", "command"])

    # Iterate over commandline arguments
    for o, a in options:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-l", "--listen"):
            listen = True

    # Checks commandline arguments, calls matching functions

    # In case user wants program to listen for incoming connections
    if listen:
        server()

main()