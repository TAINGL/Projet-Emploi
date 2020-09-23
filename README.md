# Projet Centrale d'offre d'emploi

L'objectif de ce projet est de recevoir des offres d'emploi pertinentes provenant de différents sites internet (Indeed, Monster...). L'application s'executera tous les jours à 9h.

## Installation

Pour programmer l'execution d'un fichier : CRON.
Si besoin installer l'outil, via les commandes suivantes:
```bash
apt-get install cron
```

Pour éditer les actions
```bash
export EDITOR=nano
crontab -e
```
Guide de survie de crontab : les syntaxes
```bash
# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  *  user command to be executed

mm hh jj MMM JJJ [user] tâche > log
```
-   mm : minutes (00-59).
-   hh : heures (00-23) .
-   jj : jour du mois (01-31).
-   MMM : mois (01-12 ou abréviation anglaise sur trois lettres : jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec).
-   JJJ : jour de la semaine (1-7 ou abréviation anglaise sur trois lettres : mon, tue, wed, thu, fri, sat, sun).
-   user (facultatif) : nom d'utilisateur avec lequel exécuter la tâche.
-   tâche : commande à exécuter.
-   > log (facultatif) : redirection de la sortie vers un fichier de log. Si un fichier de log n'est pas spécifié, un mail sera envoyé à l'utilisateur local.

Donc ici:
```
00 09 * * * /app.py
```

## Usage

```python

```

## Partie 1 - Scrapping (Selenium) sur Indeed

Récupération des offres d'emplois sur Indeed (bonus, si le temps = Monster).
Voici la liste des informations a récupéré :
    - titre de l'annonce
    - url de l'annonce
    - ville de l'annonce
    - le type de contrat
    - liste des thématiques/technologies

Homogénéisation des données: 

## Partie 2 - Base de données (MongoDB)

La base de donnée est en MongoDB.
Pour faire la connexion avec Flask, il y a plusieurs possibilités.
Vous pouvez utiliser l'une de ces trois bibliothèques

    Flask-PyMongo - https://flask-pymongo.readthedocs.io/en/latest/
    Flask-MongoAlchemy - https://pythonhosted.org/Flask-MongoAlchemy/
    Flask-MongoEngine - http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/

Personnellement, j'ai utilisé Flask-PyMongo.



## Partie 3 - Application (Flask)

A l'aide de l'application Flask, l'utilisateur pourra faire ces recherches pour obtenir les offres d'emploi selon ces critères:
 - mots clés
 - ville
 - titre

Le template du site web provient du site: 
https://colorlib.com/wp/free-html5-contact-form-templates/
https://colorlib.com/wp/template/responsive-table-v1/
https://colorlib.com/wp/template/careers/

## Partie 3 - Automatisation (par mail, via télégram)

Une notification est envoyé par email.