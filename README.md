
📝 Blog Article  API

Projet L2 - INF22

📌 Description du projet

Ce projet consiste en une API RESTful complète pour la gestion d'articles de blog. Développée avec FastAPI (framework Python moderne et performant), elle utilise SQLite comme système de gestion de base de données. Une interface web intuitive a été conçue pour faciliter les tests et l'utilisation des fonctionnalités.


🛠️ Technologies utilisées

Technologie Rôle
Python 3.9+ Langage de programmation principal
FastAPI Framework web (alternative moderne à Express.js)
SQLite Base de données légère (fichier unique)
Uvicorn Serveur ASGI (exécution de l'application)
HTML5 / CSS3 Interface utilisateur responsive
JavaScript Interactions dynamiques avec l'API

🚀 Installation et lancement

Prérequis

· Python 3.9 ou version ultérieure
· Pip (gestionnaire de paquets Python)

Étapes d'installation

1. Extraire ou télécharger le projet dans un dossier local.
2. Ouvrir un terminal à la racine du projet.
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Lancer le serveur :
   ```bash
   uvicorn app:app --reload
   ```
   (ou double-cliquer sur start.bat sous Windows)
5. Accéder à l'API :
   http://localhost:800

📡 Endpoints de l'API

Toutes les routes sont préfixées par /api/articles.

Méthode Route Description
POST /api/articles Créer un nouvel article
GET /api/articles Récupérer tous les articles (filtres possibles)
GET /api/articles/{id} Récupérer un article spécifique
PUT /api/articles/{id} Modifier un article existant
DELETE /api/articles/{id} Supprimer un article
GET /api/articles/search Rechercher par mot-clé dans titre/contenu

🔍 Filtres disponibles (GET /api/articles)

Paramètre Exemple Description
category ?category=Technologie Filtrer par catégorie
author ?author=Marie Filtrer par auteur
date ?date=2026-03-21 Filtrer par date

🖥️ Exemples d'utilisation

1. Interface Web Utilisateur

Ouvrir index.html dans un navigateur. L'interface permet de :

· Créer un article via un formulaire intuitif
· Visualiser la liste complète des articles
· Rechercher des articles par mot-clé
· Filtrer les articles par catégorie

2. Documentation Swagger

FastAPI génère automatiquement une documentation interactive. Accès :

```
http://localhost:8000/docs
```

Cette interface permet de tester tous les endpoints directement dans le navigateur.

3. Exemples avec cURL

Créer un article :

```bash
curl -X POST http://localhost:8000/api/articles \
  -H "Content-Type: application/json" \
  -d '{"title":"Mon premier article","content":"Contenu","author":"Moi","category":"Tech","tags":["python","fastapi"]}'
```

Lister tous les articles :

```bash
curl http://localhost:8000/api/articles
```

Rechercher un article :

```bash
curl http://localhost:8000/api/articles/search?query=pytho

🗂️ Structure des données

Chaque article est représenté par un objet JSON contenant les champs suivants :

Champ Type Description
id entier Identifiant unique (auto-incrémenté)
title chaîne Titre de l'article (obligatoire)
content chaîne Contenu de l'article (obligatoire)
author chaîne Nom de l'auteur (obligatoire)
category chaîne Catégorie de l'article (obligatoire)
tags liste Mots-clés associés (optionnel)
date chaîne Date de publication (automatique)

Exemple de réponse JSON :

```json
{
  "id": 1,
  "title": "Mon premier article",
  "content": "Ceci est le contenu de mon article",
  "author": "Marie",
  "category": "Technologie",
  "tags": ["python", "fastapi", "api"],
  "date": "2026-03-21"
}
`

📊 Codes de réponse HTTP

Code Signification
200 OK Succès (GET, PUT, DELETE)
201 Created Création réussie (POST)
400 Bad Request Requête mal formée (champs manquants)
404 Not Found Article non trouvé
500 Internal Server Error Erreur interne du serveur

📁 Structure du projet

```
Myblogapi/
├── app.py              # Code principal de l'API
├── index.html          # Interface web utilisateur
├── blog.db             # Base de données SQLite
├── requirements.txt    # Dépendances Python
├── README.md           # Documentation du projet
└── start.bat           # Script de démarrage (Windows)
```

🔧 Détails techniques

FastAPI

Framework moderne offrant :

· Documentation automatique (OpenAPI/Swagger)
· Validation des données via Pydantic
· Hautes performances (comparable à Node.js)
· Typage statique (type hints)

SQLite

Base de données embarquée :

· Fichier unique (blog.db)
· Aucune installation ou configuration supplémentaire
· Idéale pour les projets académiques

---

📈 Améliorations possibles (bonus)

· ✅ Pagination des résultats
· ✅ Authentification des utilisateurs
· ✅ Déploiement en ligne (Render.com)
· ✅ Système de commentaires
· ✅ Validation renforcée des entré

👤 Auteur

Njingang Bless Mue
Matricule : 24G2548
