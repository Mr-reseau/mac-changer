# mac-changer

Petit projet Python pour changer une adresse MAC sur une interface réseau Linux.

## Objectif
- Expliquer comment un script Python peut modifier la configuration réseau.
- Valider les entrées utilisateur et gérer les erreurs.
- Utiliser les commandes système `ip` pour désactiver/activer une interface.

## Fonctionnement du code
1. Lecture des arguments : interface et nouvelle adresse MAC.
2. Validation du format MAC : `AA:BB:CC:DD:EE:FF`.
3. Vérification des droits root.
4. Lecture de l'adresse MAC actuelle.
5. Mise hors ligne de l'interface, modification de l'adresse MAC, puis remise en ligne.
6. Vérification de l'adresse MAC finale.

## Usage
```bash
sudo python3 mac_changer.py --interface eth0 --mac 12:34:56:78:9A:BC
```

## Exemple
```bash
sudo python3 mac_changer.py -i wlan0 -m 00:11:22:33:44:55
```

## Prérequis
- Python 3
- Droits root (`sudo` sous Linux)
- Commande `ip` disponible sur le système

## Fichiers
- `mac_changer.py` : script principal
- `.gitignore` : ignore les fichiers Python compilés et les environnements

## Explication du script
- `parse_args()` : récupère les arguments CLI.
- `validate_mac()` : vérifie que l'adresse MAC est correctement formatée.
- `check_root()` : assure l'exécution en mode superutilisateur.
- `get_current_mac()` : lit la MAC actuelle via `ip link show`.
- `change_mac()` : applique la nouvelle adresse et redémarre l'interface.

## Attention
Ce script n'est utilisable que sur Linux et doit être exécuté avec prudence :
changer l'adresse MAC peut interrompre la connexion réseau.
