"""

TLS/SSL client using the builtin ssl module in Python.

Henning Thomsen

"""

import ssl
import socket

host = 'example.com'
port = 443

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
#ssl_context.load_verify_locations('/etc/ssl/cabundle.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    with ssl_context.wrap_socket(client_socket, server_hostname=host) as ssl_client_socket:
        ssl_client_socket.connect((host, port))
        ssl_client_socket.write(b'GET / HTTP1.1\n')
        print(ssl_client_socket.recv().decode())