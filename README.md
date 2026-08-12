# Django Authentication System

Système d'authentification Django générique et réutilisable avec **vérification e-mail**, **réinitialisation du mot de passe** et **envoi d'e-mails asynchrone**.

## 🎯 Présentation

Ce projet met en place un module d'authentification indépendant de toute logique métier, conçu pour être réutilisé dans différents projets Django.

Il prend en charge :

- Inscription et connexion
- Vérification du compte par e-mail
- Déconnexion
- Mot de passe oublié et réinitialisation
- Modification du mot de passe
- Protection des pages privées

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
Lorsqu'une tâche d'envoi d'e-mail est créée, elle est placée dans une file Redis en attendant d'être traitée.

### Celery

**Celery** exécute les tâches en arrière-plan grâce à un **worker séparé du serveur Django**.

Django peut donc répondre immédiatement à l'utilisateur pendant que le worker traite l'envoi de l'e-mail.

### SMTP

**SMTP** est utilisé pour effectuer l'envoi réel des e-mails vers le serveur de messagerie, par exemple Gmail ou un autre serveur SMTP.

Cette séparation permet d'obtenir :

Django → Redis → Celery Worker → SMTP → E-mail

## 🛠️ Technologies

* Python
* Django
* Celery
* Redis
* SMTP
* SQLite
* HTML / CSS

Aucun framework frontend, DRF, JWT, Docker ou RabbitMQ n'est utilisé.

## 📁 Structure

authproject/
├── accounts/       # Authentification et utilisateur
├── core/           # Pages publiques et dashboard
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

Projet en cours de développement et réalisé dans un objectif d'apprentissage de Django, de l'authentification et de l'architecture des tâches asynchrones avec **Celery + Redis + SMTP**.