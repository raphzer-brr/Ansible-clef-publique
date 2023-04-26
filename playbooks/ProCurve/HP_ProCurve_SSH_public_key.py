from __future__ import print_function
import netmiko
import os
from datetime import datetime

def get_public_key():
    with open(os.path.expanduser("~/.ssh/id_rsa.pub")) as f:
        public_key = f.read().strip()
    return public_key

def configure_hp_procurve(hpProcurvesLocal):
    public_key = get_public_key()
    commands = [
        "no telnet-server",
        "ip ssh port 22",
        "ip ssh cipher aes256-cbc",
        "ip ssh mac hmac-sha1",
        "ip ssh filetransfer",
        "aaa authentication ssh login public-key none",
        "aaa authentication ssh enable public-key"
        #"crypto key generate ssh rsa bits 3072", Il faudrait pouvoir regenéré la clef ssh avec le max de bit possible si cela n'a pas été fait comme ca mais cette commande risque de faire platé le programme
    ]
    try:
        with netmiko.ConnectHandler(**hpProcurvesLocal) as connection:
            start_time = datetime.now()
            print(f"Prompt de départ : {connection.find_prompt()}")
            output = connection.send_config_set(commands)
            try:
                output += connection.send_config_set(f"ip ssh public-key manager '{public_key}'")
            except netmiko.exceptions.ReadTimeout:
                print(f"""La connexion a expiré en raison d'une attente trop longue, \nvérifie que la clef public est bien dans le switch

    Commande de vérification : 
                show crypto client-public-key
                ssh -i /path/to/myprivatekey {hpProcurvesLocal["ip"]}@{hpProcurvesLocal["ip"]} 
                """)
            end_time = datetime.now()
        print(output)
        print(f"Exec time for 1 device: {end_time - start_time}")
    except netmiko.exceptions.NetmikoAuthenticationException as e:
        err = str(e).replace("Authentication to device failed.\n", "").replace("Common causes of this problem are:\n", "")
        print(f"Message personnel de debug : \n0. L'authentification par clef publique est déjà déployer\n\nMessage de Netmiko: {err}")
def main():
    hpProcurves = {
        "ip":'192.168.1.22',
        "device_type":'hp_procurve',
        "username":'admin',
        "port":'22',
        "password":os.environ["PWD_HP"],
        "session_log": "netmiko_session.log"
    }
    start_time_tot = datetime.now()
    configure_hp_procurve(hpProcurves)
    end_time_tot = datetime.now()
    print(f"Exec time tot: {end_time_tot - start_time_tot}")

if __name__ == "__main__":
    main()


# ipfile=open("iplist.txt") #This file contains a list of switch ip addresses.
# configfile=open("configfile.txt") #opening the config file with the changes you want to push
# configset=configfile.read() ##reads the config file
# configfile.close() #closes the config file


# output = connection.send_config_set(commands)
# output += connection.send_config_set(f"ip ssh public-key manager '{public_key}'")
# print(output)
# # Déconnexion
# connection.disconnect()