"""

Example SSH client where it is possible to run multiple commands.

Uses the Paramiko module.
Uses password based authentication.

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

def run_command(command):
    print("Runing command", command)
    stdin, stdout, stderr = ssh_client.exec_command(command)

    # Print command output
    print("stdout: ", stdout.read().decode())
    print("stderr: ", stderr.read().decode())

with paramiko.SSHClient() as ssh_client:

    #ssh_client = paramiko.SSHClient()

    # Load host keys
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Not very secure

    # Connects to remote client
    ssh_client.connect(hostname=ssh_host, port=ssh_port, username=username, password=password, look_for_keys=False)

    # Sends commands to client (via stdin), receives command output (from stdout and stderr)
    # We can't use exec_command(), because the transport (=connection) is closed when we call it once.

    # Run pwd command
    # command = "pwd"
    # print("Runing command", command)
    # stdin, stdout, stderr = ssh_client.exec_command(command)

    # # Print command output
    # print("stdout: ", stdout.read().decode())
    # print("stderr: ", stderr.read().decode())
    command = ""

    while command.lower() != 'q':
        command = input("Enter command, q to quit: ")
        if command.lower() == 'q':
            break            
        run_command(command)

    # Closes the connection
    #ssh_client.close()