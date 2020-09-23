"""
Example with an interactive shell using Paramiko

Based on: https://github.com/paramiko/paramiko/blob/master/demos/demo_simple.py

Henning Thomsen
"""

import sys
import os
import paramiko
import Interactive

# From https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script/4060259#4060259
__location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)) )

credentialFile = "sshCredentials.txt"

credentials = []

# Load hostname and credentials from external file
with open(os.path.join(__location__, credentialFile), mode="r") as f:
    for line in f:
        credentials.append(line.rstrip())
ssh_host = credentials[0]
ssh_port = int(credentials[1])
username = credentials[2]
password = credentials[3]

with paramiko.SSHClient() as ssh_client:
    # Load host keys
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Not very secure

    # Connects to remote client
    ssh_client.connect(hostname=ssh_host, port=ssh_port, username=username, password=password, look_for_keys=False)

    # Run interactive shell
    
    # Here we need to exchange data
