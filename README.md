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
├── accounts/       # Authentification, utilisateur, formulaires, vues et tâches
├── core/           # Pages publiques, dashboard et configuration de l'application
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

## 🚧 État du projet

Projet en cours de développement et réalisé dans un objectif d'apprentissage approfondi de Django, de l'authentification et de l'architecture des tâches asynchrones avec **Celery + Redis + SMTP**.

Les principales bases du système sont désormais en place : modèles utilisateurs, formulaires d'authentification, vues, URLs, gestion des tokens, tâches Celery ainsi que les premiers templates pour l'accueil, la connexion et le tableau de bord.

Le développement se poursuit avec l'intégration complète des différents flux d'authentification, la configuration des e-mails et les tests du système.