#!/usr/bin/env python3
"""

Basic TCP client using the socket module.
This client sends data (in the form of strings 
from command line) to the server.

Example usage:
Sends "Hello world" to localhost TCP server on port 8000.
./client.py -s Hello world -t 127.0.0.1 -p 8000

By: Henning Thomsen

"""

# Standard library imports
import socket
import sys

# Third party imports
import getopt

target = ""
port = 0
cmdstring = ""

def usage():
    print("Client, example usage:")
    print("./client.py -s \"Hello world\" -t 127.0.0.1 -p 8000")
    print("Sends \"Hello world\" to localhost TCP server on port 8000")

def client():
    """
    Creates client socket sending cmd-line argument to server on specified port
    """
    print("Sending %s to %s:%i" % (cmdstring, target, port))
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((target, port))

    client.send(cmdstring.encode())

def main():
    """
    Main function, parses command-line arguments using getopt
    """
    global target
    global port
    global cmdstring

    options, args = getopt.getopt(sys.argv[1:], "hs:t:p:", ["help", "string", "target", "port"])

    for o, a in options:

        if o in ("-h", "--help"):
            usage()

        elif o in ("-t", "--target"):
            target = str(a)

        elif o in ("-p", "--port"):
            port = int(a)

        elif o in ("-s", "--string"):
            cmdstring = str(a)

    if port > 0:
        client()

main()