# Theseus IHM

## Installation
Utiliser Poetry pour gérer les dépendances:
```bash
poetry install
```



## Schéma global:

- Vue globale: ensemble de la carte
- Vue piege: Reperé, actionné, desactivé
- Ajout de zone interdite
- Modification GPS
- établissement de route


# Organisation des fichiers:
- apis:
  - version1:
    - route_general_pages.py: routes vers les pages avec template et/ou statiques 
    - route_markers.py: routes api REST des marqueurs de la cartes
- core:
  - models:
  - repository:
- db: interations avec la base de données (fichier sqlite)
- schemas:
  - markers.py
- static: Fichiers statiques du site web
  - images
- templates: page Html de templates (squelettes)

# Base de données
## baptemes: 
contient les baptèmes terrain.

data: 
- nom: nom du baptème terrain
- type: point, ligne ou zone
- longitude
- latitude

plusieurs entrées de même nom définissent les points suivant () 

## Satellites:
contient la position des satellites

data:
- nom: nom du satellite
- longitude
- latitude
- altitude
- vitesse
- direction
- niveau de batterie
- timestamp

Le timestamp est la date de la date mise à jour de la position du satellite,
et permet de suivre le parcours du satellite dans le temps.

## Marqueurs:
contient les marqueurs de la carte, pour l'instant les pièges

data:
- nom: nom du piège
- longitude
- latitude
