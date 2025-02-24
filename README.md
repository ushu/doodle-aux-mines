# Doodle or Die Clone

Un clone du jeu [Doodle or Die](https://doodleordie.com) où les joueurs créent des chaînes de dessins et de légendes qui s'alternent.

## Description

Ce projet est une réimplémentation du concept de Doodle or Die, développée avec :
- FastAPI pour l'API backend
- SQLite pour la persistance des données
- Templates Jinja2 pour le rendu frontend

## Fonctionnalités

- Création de chaînes de dessins et descriptions
- Interface de dessin interactive
- Système d'authentification utilisateur
- Stockage des dessins et des chaînes dans SQLite

## Installation

1. Récupérer le code de l'exemple
   npx degit https://github.com/ushu/doodle-aux-mines

2. Installer les dépendances
   uv pip install -r requirements.txt

3. Lancer le serveur
   uv run fastapi dev main.py

## Technologies Utilisées

- Backend : FastAPI
- Base de données : SQLite
- Frontend : HTML/CSS/JavaScript
- Templates : Jinja2

## Contexte Pédagogique

Ce projet est destiné aux élèves de première année de Mines ParisTech dans le cadre de leur formation en développement web. Il sert de support pédagogique pour l'apprentissage des technologies web modernes.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une pull request.

## Licence

MIT
