# Ansible-clef-publique

## Todo
- [ ]  METTRE A JOUR LE README !!!!!!!!!
- [ ]  Mettre en place un seveur dedier ansible sous deb 11 avec comme base l’article suivant : [https://www.tutos.eu/7852](https://www.tutos.eu/7852)
- [ ]  Faire des fichier yaml qui serviront de var d'env pour des groupes d'apareil suivant leur OS
- [ ]  Metre en place un script qui supprime les backup de fichier de conf trop vielle 
- [x]  Réfléchir si il serait mieux de mettre tout le deploiment dans un seule fichier : **OUI**
- [x]  Mettre en place des variable d’environnment pour pouvoire faire mes git push l’esprit trkl
- [x]  Tester si l’os de l’appareil il est bien celui adapté.

## Cette grosse plaie de HP procurve 
Liste des problemes : 
- [ ]  Pas de module ansible officiel si je ne m'abuse (Aruba possible mais ProCurve dans mes reves)
- [ ]  Pourquoi pas le faire a la main en python ? => Des gens bien plus chaud que moi n'ont pas réussit 
- [ ]  Reverse engenering sur la maniere dont les commande ssh sont envoyer au switch via wireshark ! Sauf que devine quoi c'est impossible selon le Wiki de Wireshark (satané Diffie Helman)
- [ ]  Pourquoi pas changer le temps de négotiation de clef ???
- [ ]  Changer vers un algorithme obsolet ??
- [ ]  Trouver un autre bail de Ansible (Puppet ?? Terraforme ??)
- [ ]  Executé des commande via python comme si j'etais dans un terminale ??????? => Best soluc pour l'instant  

### Solution : ⭐ netmiko ⭐
**Todo**
- [ ] Transphormé en commande le script 
- [ ] Si aucune clef est créé il faut qu'il en génère une ssh ssh-keygen -t rsa -b 4096 ou au moins qu'il affiche la commande ssh-keygen -t rsa -b 4096
- [ ] Faire en sorte que les arg -p ou --port, -k ou --pub-key , -d ou --device (dictionnaire d'IP), -i ou --inventory
- [ ] Faire ne
- [ ] Il faut qu'il soit capable d'itéré cela sur plusieur HP procurve 
- [ ] Trouver un moyen de centralisé tout les hoste dans un fichier hosts.yaml et meme ceux HP
- [ ] Faire un vrai test avec les clef publique pour afficher seulement les erreur de Netmiko
- [ ] Trouver un moyen de regler sans try exept le probeleme de timeout 
- [ ] utilisé shell dans le playbook pour pouvoir run le script 
- [x] Trouver l'erreur qui empeche de voire le resultat des commande en console 
- [x] Trouver un moyen de supprimer la clef public client de maniere a pouvoire en mettre une autre 
- [x] Faire ensuite un jeu de commande pour remettre le switch dans sa configuration de depart avec une auth ssh par mot de passe 

**Intallation**
```bash
pip install netmiko
pip install paramiko --upgrade
```
**Variable d'environnement**
```bash
export PWD_HP="Mon Mot de passe"
```
```bash
echo 'PWD_HP="Mon Mot de passe"'>>~/.zshrc && source ~/.zshrc
```
**Anulation du script**
```
no ip ssh filetransfer
ip ssh
aaa authentication ssh login local none
aaa authentication ssh enable local none
clear crypto client-public-key manager 0

```

## NX OS
### Todo

- [ ]  Demandé à l’utilisateur le chemin vers sa clef publique, ou trouver le moyen de foutre un arg dans la commande ansible-playbooks
- [ ]  Demandé a l’utilisateur si il souhaite sécurisé son accès ssh ou si oui fait une ACL assisté a base de question et de varible comme ansible_host pour l’@IP du SW ou avec vrf mgmt
- [x]  Enregister apres avoire effectuer des configuration
- [x]  Supprimé l’utilisateur avant de le créé
- [x]  Faire en sorte d’enregistrer le fichier de configuration précédent avant toute configuration avec ansible

### 🆘 Todo oubliette / idée avorté 🆘
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
    - Generale : 
        - Optimisation [lien](https://www.redhat.com/sysadmin/faster-ansible-playbook-execution) et [lien][lien](https://www.redhat.com/sysadmin/faster-ansible-modules)  
    - IOS : [lien](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_command_module.html)
        - Vidéo : [lien](https://youtu.be/wbVZkb8ocH4)
    - NX OS :
        - Doc [lien](https://docs.ansible.com/ansible/latest/collections/cisco/nxos/index.html)
        - ✨ : [lien](https://docs.ansible.com/ansible/latest/collections/cisco/nxos/nxos_command_module.html)
        - Exemple (old donc ~) : [lien](https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html#play)
