#!/usr/bin/env python3
"""

Basic TCP server using the socket module.
Possible to specify which TCP port to listen 
to via command-line.
Only one thread is used for serving connecting clients.
Only listens on localhost interface.

The program takes the following arguments
-p: port number

Example usage:
Listen for incoming connection on port 8000
./server.py -p 8000

By: Henning Thomsen

"""

# Standard library imports
import socket
import sys

# Third party imports
import getopt

localhost = "127.0.0.1"
#allhosts = "0.0.0.0" # Not used atm.
port = 0

def usage():

    # TODO: Add more usage example as more features are added.

    print("Example usage: ")
    print("./server.py -p 8000: Listen on port 8000")

def server():

    while True:

        # Serve client
        print("Listening for incoming connections on port %i." % int(port))

        # Create listening socket:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket to IP and port (only listen on localhost)
        server_socket.bind((localhost, int(port)))

        # Listen for incoming connections
        server_socket.listen(1)

        client, addr = server_socket.accept()
        print("Client %s connected on port %s" % (addr[0], addr[1]))
        
        while True:
            # Receive data
            request = client.recv(1024)
            
            # Print what was received
            print("Received data: %s" % str(request.decode()))

            # Close socket when data is exhausted
            if not request:
                client.close()

                server_socket.close()

                break

def main():
    """
    Main function which is called with cmd-line arguments on startup
    """
    global port

    # Parse arguments using getopt
    options, args = getopt.getopt(sys.argv[1:], "hp:", ["help", "port"])

    for o, a in options:

        if o in ("-h", "--help"):
            usage()

        elif o in ("-p", "--port"):
            port = int(a)

    server()

main()