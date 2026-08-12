# Django Authentication System

Système d'authentification Django générique et réutilisable avec **vérification e-mail**, **réinitialisation du mot de passe** et **envoi d'e-mails asynchrone**.

## 🎯 Présentation

Ce projet met en place un module d'authentification indépendant de toute logique métier, conçu pour être réutilisé dans différents projets Django.

L'objectif est de construire progressivement une architecture propre, maintenable et suffisamment générique pour pouvoir être intégrée à différents projets.

Il prend en charge :

- Inscription et connexion
- Vérification du compte par e-mail
- Déconnexion
- Mot de passe oublié et réinitialisation
- Modification du mot de passe
- Protection des pages privées
- Pages d'accueil et tableau de bord
- Formulaires Django dédiés à l'authentification
- Gestion des tokens de vérification et de réinitialisation
- Envoi des e-mails en arrière-plan avec Celery

## ⚙️ Architecture asynchrone

L'objectif principal du projet est de ne jamais bloquer une requête Django pendant l'envoi d'un e-mail.

Utilisateur
│
▼
Django
│
│ .delay()
▼
Redis
(Broker)
│
▼
Celery Worker
│
│ send_mail()
▼
SMTP
│
▼
Boîte e-mail

### Redis

**Redis** sert de **broker** entre Django et Celery.

Lorsqu'une tâche d'envoi d'e-mail est créée, elle est placée dans une file Redis en attendant d'être traitée par un worker Celery.

### Celery

**Celery** exécute les tâches en arrière-plan grâce à un **worker séparé du serveur Django**.

Django peut donc répondre immédiatement à l'utilisateur pendant que le worker traite l'envoi de l'e-mail.

Les tâches d'envoi sont également configurées avec un mécanisme de **retry**, permettant de retenter automatiquement l'envoi en cas d'échec temporaire du serveur SMTP.

### SMTP

**SMTP** est utilisé pour effectuer l'envoi réel des e-mails vers le serveur de messagerie, par exemple Gmail ou un autre serveur SMTP.

Cette séparation permet d'obtenir :

Django → Redis → Celery Worker → SMTP → E-mail

## 🔐 Authentification

Le système utilise les mécanismes d'authentification fournis par Django tout en ajoutant une logique spécifique au projet.

Le compte nouvellement créé reste inactif jusqu'à la confirmation de son adresse e-mail. Des tokens sont utilisés pour sécuriser les liens de vérification et de réinitialisation du mot de passe.

Les formulaires personnalisés permettent notamment de gérer :

- La création d'un compte avec adresse e-mail
- La vérification de l'unicité de l'adresse e-mail
- La connexion des utilisateurs actifs
- La demande de réinitialisation du mot de passe
- La modification du mot de passe

## 🖥️ Interface

Le projet dispose désormais d'une première interface HTML basée sur des templates Django.

Les principales pages comprennent :

- Page d'accueil
- Tableau de bord protégé
- Inscription
- Connexion
- Confirmation d'envoi de l'e-mail d'activation
- Lien de vérification invalide ou expiré
- Mot de passe oublié
- Confirmation d'envoi de l'e-mail de réinitialisation
- Réinitialisation du mot de passe
- Réinitialisation invalide ou expirée
- Réinitialisation terminée
- Modification du mot de passe

Les templates utilisent un template de base commun ainsi que des fichiers CSS dédiés.

## 🛠️ Technologies

- Python
- Django
- Celery
- Redis
- SMTP
- SQLite
- HTML / CSS

Aucun framework frontend, DRF, JWT, Docker ou RabbitMQ n'est utilisé.

## 📁 Structure

authproject/
├── accounts/       # Utilisateur, authentification, formulaires, vues et tâches
├── core/           # Accueil et tableau de bord
├── config/         # Configuration Django + Celery
├── templates/      # Templates HTML et e-mails
├── static/         # CSS et fichiers statiques
├── .env            # Variables d'environnement
├── .env.example
├── manage.py
└── requirements.txt

## 🚀 Lancement

Installer les dépendances :

pip install -r requirements.txt

Appliquer les migrations :

python manage.py migrate

Lancer Redis :

redis-server

Lancer le worker Celery :

celery -A config worker --loglevel=info

Puis lancer Django :

python manage.py runserver

Trois processus doivent fonctionner simultanément :

- Redis pour gérer la file de messages
- Celery Worker pour exécuter les tâches en arrière-plan
- Django pour gérer les requêtes HTTP

## 🚧 État du projet

Projet en cours de développement et réalisé dans un objectif d'apprentissage approfondi de Django, de l'authentification et de l'architecture des tâches asynchrones avec **Celery + Redis + SMTP**.

Les principales bases du système sont désormais en place : modèle utilisateur personnalisé, formulaires, vues, URLs, gestion des tokens, tâches Celery, templates d'authentification, pages publiques et tableau de bord protégé.

Le prochain objectif est de réaliser les **tests complets des différents flux d'authentification**, notamment l'inscription, la vérification e-mail, la connexion, la réinitialisation du mot de passe et l'envoi asynchrone des e-mails.