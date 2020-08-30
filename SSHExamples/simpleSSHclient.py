#!/usr/bin/env python3
"""
Simple SSH client example.
Connects to a remote SSH server 
using the Paramiko library.

This version only uses username,password authentication.

Henning Thomsen
"""

import sys
import os
import paramiko

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

ssh_client = paramiko.SSHClient()

# Load host keys
ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Not very secure

# Connects to remote client
ssh_client.connect(hostname=ssh_host, port=ssh_port, username=username, password=password, look_for_keys=False)

# Run pwd command
stdin, stdout, stderr = ssh_client.exec_command("pwd")

# Print command output
print("stdout: %s" % stdout.read().decode())
print("stderr: %s" % stderr.read().decode())