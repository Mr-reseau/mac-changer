# mac-changer

Petit projet pour modifier l'adresse MAC d'une interface réseau sur Linux.

## Objectif
- Permettre le changement d'adresse MAC d'une interface réseau.
- Fournir une solution simple en Python pour les environnements Linux.

## Usage
```bash
sudo python3 mac_changer.py --interface eth0 --mac 12:34:56:78:9A:BC
```

## Prérequis
- Python 3
- Doit être exécuté avec des droits root
- Système Linux avec `ip` installé

## Fichiers
- `mac_changer.py` : script principal
- `.gitignore` : fichiers à ignorer dans Git
