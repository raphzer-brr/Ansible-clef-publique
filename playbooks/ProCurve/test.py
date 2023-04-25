from __future__ import print_function
import netmiko
import os
from getpass import getpass

with open(os.path.expanduser("~/.ssh/id_rsa.pub")) as f:
    public_key = f.read().strip()

print(f"ip ssh public-key manager '{public_key}'")

connection = netmiko.ConnectHandler(
    ip='192.168.1.22',
    device_type='hp_procurve',
    username='admin',
    port='22',
    password='cisco',
)


commands = [
    "no telnet-server",
    "ip ssh port 22",
    "ip ssh cipher aes256-cbc",
    "ip ssh filetransfer",
    "aaa authentication ssh login public-key",
    "aaa authentication ssh enable public-key",
    "crypto key zeroize ssh-client-key",
    "crypto key zeroize ssh",
    "crypto key generate ssh rsa bits 3072",
    f"ip ssh public-key manager '{public_key}'"
]

output = connection.send_config_set(commands)

# Déconnexion
connection.disconnect()
