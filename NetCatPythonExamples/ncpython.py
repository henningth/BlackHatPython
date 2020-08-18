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
import subprocess
import sys
import threading

# Third party imports
import getopt

# Global variables
target = ""
port = 0
listen = False
upload_file = ""
command = False

def usage():
    """
    Prints usage
    """
    print("Netcat-inspired implementation in Python.")
    print("Usage: ./ncpython.py -t target -p port <commands>")
    print("Here <commands can be be one of:>")
    print("-l: listen for incoming connections (server mode)")
    print("-u <filename>: saves received file contents in <filename> (server mode)")
    print("-u <filename>: upload file to remote server (client mode)")
    print("-c: return a command shell (client mode)")
    print("-h: prints usage (both client, server)")

def client():
    """
    This is called when program is in client mode
    (using the commands u and c.)
    """

    # Connects to server
    client_socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
    client_socket.connect((target, port))

    print("client mode.")
    if command:
        """
        User sends commands to server
        """
        print("Sends commands to server.")
        # User enters a command
        #command_string = sys.stdin.read().encode()

        while True:
            command_string = input("<CMD>: ").encode()

            # Sends command
            client_socket.send(command_string)

            # Receives result
            result = client_socket.recv(1024)
            print("Result: ")
            print(result.decode())

    if len(upload_file) > 0:
        """
        Uploads file to server
        """
        print("Sends file to server.")

        # Uploads file
        with open(upload_file, "rb") as f:
            byte = f.read(1024)
            while byte: # Read until byte is empty
                # Send byte
                client_socket.send(byte)
                
                # Read next 1024 bytes
                byte = f.read(1024)


def run_command(command_string):
    """
    Runs command (on server), retuns result (to client)
    """
    command_string = command_string.rstrip() # Remove newline
    try:
        result = subprocess.check_output(command_string, stderr = subprocess.STDOUT, shell=True)
    except Exception as e:
        print("Failed to run command, error message: ")
        print(e)
    return result

def client_handler(client_socket):
    """
    Client handling process, spawned when client 
    connects to listening server
    """
    if command:
        print("Receives commands from client.")
        # Receive commands from client, 
        # return results to it.
        while True:
            command_string = ""
            while "\n" not in command_string:
                byte = client_socket.recv(1024)
                command_string += byte.decode()
                if len(byte) < 1024:
                    break
            print("Received command: ", command_string)
            # Execute command
            result = run_command(command_string)
            if result:
                # Send result of command to client
                print("Sends result to client.")
                client_socket.send(result)


    if len(upload_file) > 0:
        print("Receives file from client.")
        # Receive file from client, saves it, 
        # and returns status.
        with open(upload_file, "wb") as f:
            # Receive byte
            while True:
                byte = client_socket.recv(1024)
                f.write(byte)
                if len(byte) < 1024:
                    break


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
    global upload_file
    global command

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
        elif o in ("-u", "--upload"):
            upload_file = a
        elif o in ("-c", "--command"):
            command = True

    # Checks commandline arguments, calls matching functions

    # In case user wants program to listen for incoming connections
    if listen:
        server()

    if not listen:
        client()

main()