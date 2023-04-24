# Ansible-clef-publique

## Todo

- [ ]  Mettre en place des variable d’environnment pour pouvoire faire mes git push l’esprit trkl
- [ ]  Mettre en place un seveur dedier ansible sous deb 11 avec comme base l’article suivant : [https://www.tutos.eu/7852](https://www.tutos.eu/7852)
- [ ]  Réfléchir si il serait mieux de mettre tout le deploiment dans un seule fichier et de tester si l’os de l’appareil il est bien celui adapté.
- [ ]  Faire des fichier yaml qui serviront de var d'env pour des groupes d'apareil suivant leur OS


## NX OS

- [ ]  Enregister apres avoire effectuer des configuration
- [ ]  Supprimé l’utilisateur avant de le créé
- [ ]  Demandé à l’utilisateur le chemin vers sa clef publique, ou trouver le moyen de foutre un arg dans la commande ansible-playbooks
- [ ]  Faire en sorte d’enregistrer le fichier de configuration précédent avant toute configuration avec ansible
- [ ]  Demandé a l’utilisateur si il souhaite sécurisé son accès ssh ou si oui fait une ACL assisté a base de question et de varible comme ansible_host pour l’@IP du SW ou avec vrf mgmt
- [ ]  Mettre a jour le N5K car pour celui que j’utilise on est a la version 5.3….

| Supported Platforms | Minimum NX-OS Version |
| --- | --- |
| Cisco Nexus N3k | 7.0(3)I2(5) and later |
| Cisco Nexus N9k | 7.0(3)I2(5) and later |
| Cisco Nexus N5k | 7.3(0)N1(1) and later |
| Cisco Nexus N6k | 7.3(0)N1(1) and later |
| Cisco Nexus N7k | 7.3(0)D1(1) and later |

### Install module NX-OS

```bash
ansible-galaxy collection install cisco.nxos &&
pip install ansible-pylibssh
```

---

### Commande de deploiment

```bash
cd ~/Projects/Ansible-clef-publique
ansible-playbook playbooks/NX-OS/SSH_public_key.yaml -i hosts.yaml
```

### hosts.yaml

```yaml
---
nxos:
  hosts:
    nx-1:
      ansible_port: 22
      ansible_host: 192.168.1.248
      ansible_connection: ansible.netcommon.network_cli
      ansible_ssh_user: admin
      ansible_network_os: cisco.nxos.nxos
      ansible_ssh_pass: Cisco123cisco
      ansible_ssh_common_args: -oHostKeyAlgorithms=+ssh-rsa
```

### SSH_public_key.yaml

```yaml
# ====================== TO DO ====================== #

# ==================== ❌ ou ✅ ===================== #

---
  - name: Deploiment de clef publique SSH sur NX OS
    hosts: nxos
    gather_facts: false
    
    vars_prompt:
    # Doc : https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_prompts.html
      - name: username
        prompt: Entrer un username pour l'accès SSH sur le switch. default
        private: false
        default: "sshuser"

    vars:
      ssh_key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}" # Récupération de la clé publique SSH dans l'hote Ansible avec le chemin indiqué, faire attention au droit de lecture 

# ====================== PAS ENCORE TEST ====================== #
    # tasks:
    #   - name: Sauvegarde de la configuration avant changement
    #     cisco.nxos.nxos_config:
    #       backup: yes
    #       backup_options:
    #         filename: backup.cfg
    #         dir_path: /home/raphael/NX/
# ============================================================== #

      - name: Désactivation telnet
        cisco.nxos.nxos_feature:
          feature: telnet
          state: disabled
      
      - name: Création de l'utilisateur SSH
        cisco.nxos.nxos_command:
          commands:
          - configure terminal
          - command: "username {{ username }} role network-admin"
      
      - name: Ajout de la clef publique sur le switch depuis ~/.ssh/id_rsa.pub
        cisco.nxos.nxos_command:
          commands:
          - configure terminal
          - command: "username {{ username }} sshkey {{ ssh_key }}"  
          # Utilisation de la variable ssh_key contenant la clé publique
            
      - name: Création d'un couple de clef RSA (2048 bits) sur le switch 
        cisco.nxos.nxos_command:
          commands:
          - configure terminal
          - command: "username {{ username }} keypair generate rsa 2048 force"

# ====================== PAS ENCORE TEST ====================== #
      # - name: Enregistrement de la configuration
      #   cisco.nxos.nxos_command:
      #     commands:
      #     - copy running-config startup-config

      # OU

      # - name: Save configuration
      #   cisco.nxos.nxos_save_config:
# ============================================================== 
```

## Methode de versionning des fichiers de configuration (Pour la PoC seulement)

### Mise en place du versionning des fichier de configuration

- **Memoire interne**
    - NX OS
    
    ```
    copy running-config bootflash:base.conf
    ```
    
    ---
    
    - HP
    
    ```
    A FAIIIIIIRE
    ```
    
    ---
    
    - IOS
    
    ```
    copy running-config flash://base.conf
    ```
    
- **TFTP admin**
    - NX OS
    
    ```
    copy running-config tftp://10.100.40.95/NX.conf vrf management
    ```
    
    - HP
    
    ```
    A FAIIIIIIRE
    ```
    
    - IOS
    
    ```bash
    copy running-config tftp://10.100.40.95/IOS.conf
    ```
    

### Récuperation de la version de base

- **Memoire interne**
    - NX OS
    
    ```
    copy bootflash:base.conf running-config 
    ```
    
    ---
    
    - HP
    
    ```
    A FAIIIIIIRE
    ```
    
    ---
    
    - IOS
    
    ```
    copy flash://base.conf running-config 
    ```
    
- **TFTP admin**
    - NX OS
    
    ```
    copy tftp://10.100.40.95/NX.conf running-config  vrf management
    ```
    
    - HP
    
    ```
    A FAIIIIIIRE
    ```
    
    - IOS
    
    ```bash
    copy tftp://10.100.40.95/IOS.conf running-config 
    ```
    

## Lien utile

- **Comprendre le YAML : [lien](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html#yaml-syntax)**
- **Bonne pratique Ansible : [lien](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)**
- **Cisco**
    - IOS : [lien](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_command_module.html)
        - Vidéo : [lien](https://youtu.be/wbVZkb8ocH4)
    - NX OS :
        - Doc [lien](https://docs.ansible.com/ansible/latest/collections/cisco/nxos/index.html)
        - ✨ : [lien](https://docs.ansible.com/ansible/latest/collections/cisco/nxos/nxos_command_module.html)
        - Exemple (old donc ~) : [lien](https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html#play)
