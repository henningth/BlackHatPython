#!/usr/bin/env python3
"""

Basic TCP server using the socket module.
Possible to specify which TCP port to listen 
to via command-line.
Only one thread is used for serving connecting clients.

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

def usage():

    print("Example usage: ")
    print("./server.py -p 8000: Listen on port 8000")

def server(port):

    # Serve client
    print("Listening for incoming connections on port %i." % int(port))

def main():
    """
    Main function which is called with cmd-line arguments on startup
    """

    # Parse arguments using getopt
    options, args = getopt.getopt(sys.argv[1:], "hp:", ["help", "port"])

    for o, a in options:

        if o in ('-h', '--help'):
            usage()

        if o in ('-p', '--port'):
            server(a)

main()