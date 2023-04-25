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
    password=getpass('Enter a password for the switch:\n')
)


connection.send_command("no telnet-server")
connection.send_command("ip ssh port 22")
connection.send_command("ip ssh cipher aes256-cbc")
#connection.send_command("ip ssh filetransfer")
connection.send_command("aaa authentication ssh login public-key")
connection.send_command("aaa authentication ssh enable public-key")
connection.send_command("crypto key zeroize ssh-client-key")
connection.send_command("crypto key zeroize ssh")
connection.send_command("crypto key generate ssh rsa bits 3072")
connection.send_command_timing(f"ip ssh public-key manager '{public_key}'", delay_factor=2)



# Déconnexion
connection.disconnect()
