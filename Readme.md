# Theseus IHM

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

plusieurs entrée de même nom définissent les points suivant () 

API:
- 