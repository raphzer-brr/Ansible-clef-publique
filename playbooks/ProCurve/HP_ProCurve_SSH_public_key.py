from __future__ import print_function
from datetime import datetime
from colorama import Fore, Back, Style
import sys
import netmiko
import os


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
            output = connection.send_config_set(commands)
            try:
                output += connection.send_config_set(f"ip ssh public-key manager '{public_key}'")
            except netmiko.exceptions.ReadTimeout:
                timeout = True
                print(f"{Back.BLUE}Déploiment réussit !{Style.RESET_ALL} : Petit soucis de timeout mais rien de grave\n")
                print(f"{Fore.BLUE}Commande de vérification : {Style.RESET_ALL}")
                print("show crypto client-public-key")
                print(f"ssh -i /path/to/myprivatekey {hpProcurvesLocal['ip']}@{hpProcurvesLocal['ip']}\n")
            end_time = datetime.now()
        if (not timeout):
            print(f"{Back.BLUE}Déploiment réussit !{Style.RESET_ALL} : Tout est OK")
        print(f"{Fore.BLUE}Commande effectué : {Style.RESET_ALL}{output}")
        print(f"{Back.MAGENTA}Benchmark{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'Exec time for 1 device : ':<25}{Style.RESET_ALL}{end_time - start_time}")

    except netmiko.exceptions.NetmikoAuthenticationException as e:
        err = str(e).replace("Authentication to device failed.\n", "").replace("Common causes of this problem are:\n", "").replace("\n\n\nAuthentication failed.", "").replace("\nDevice settings: hp_procurve 192.168.1.22:22", "")
        print(f"{Back.RED}ERREUR{Style.RESET_ALL}: Authentification Fail")
        print(f"{Fore.RED}Message personnel de debug :{Style.RESET_ALL}\n0. L'authentification par clef publique est déjà déployer\n")
        print(f"{Fore.RED}Message de Netmiko:{Style.RESET_ALL} {err}\n")
        sys.exit(1)
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
    print(f"{Fore.MAGENTA}{'Exec time tot : ':<25}{Style.RESET_ALL}{end_time_tot - start_time_tot}")

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