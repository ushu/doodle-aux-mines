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
- Stockage des dessins et des chaînes dans SQLite

## Installation

1. Récupérer le code de l'exemple
   ```bash
   npx degit https://github.com/ushu/doodle-aux-mines
   ```

2. Installer les dépendances
   ```bash
   uv sync
   ```

3. Créér la base
   ```bash
   uv run db/seed.py
   ```

4. Lancer le serveur:

   - en mode *dev*
     ```bash
     uv run fastapi dev main.py
     ```
   - en mode *prod*
     ```bash
     uv run main.py
     ```

## Lancer les tests

Ce projet propose quelques tests simples (pour les requêtes en base) dans le répertoire `test/`.

Pour les exécuter:
```bash
uv run pytest
```

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
