"""
SSH client using Paramiko module.
Authenticates with a remote server using 
the server's public key.

Henning Thomsen
"""

import paramiko

import os

__location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)) )

ssh_client = paramiko.SSHClient()

ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Not very secure

hostname = "192.168.1.150"
username = "henning"
port = 22
key_filename = "id_rsa.priv" # On Win 10: Generated using PuTTY key generator, using Conversions -> Export OpenSSH key

private_key = paramiko.RSAKey.from_private_key_file(filename=os.path.join(__location__, key_filename))

print("Connecting to: %s" % hostname)
ssh_client.connect(hostname=hostname, username=username, port=port, pkey=private_key)

remote_command = "pwd"

print("Running command %s on remote machine." % remote_command)
stdin, stdout, stderr = ssh_client.exec_command(remote_command)

print("stdout: %s" % stdout.read().decode())
print("stderr: %s" % stderr.read().decode())

ssh_client.close()