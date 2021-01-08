# Projet 2 Openclassrooms - Scraping avec Beautifulsoup

## Définition et objectif du projet 2
Le projet 2 d'Openclassrooms vise à utiliser les bases du langage Python pour effectuer le scraping (extraction de contenu) du site [https://books.toscrape.com/](https://books.toscrape.com/)

## Plan général
1. Utilité et création d'un environnement virtuel
2. Installation des modules requis
3. Execution et fonctionnement du code

## 1) Utilité et création d'un environnement virtuel
Un environnement virtuel est un répertoire contenant une installation de Python autonome. Il est coutume de créer un environnement virtuel pour chaque projet.
Chaque environnement virtuel comprend sa propre version de Python et tous les paquets Python que vous décidez d'y installer.

Pour créer un environnement virtuel, il faut utiliser module Python *venv* disponible à partir de la version 3.3 de Python

Pour la création de l'environnement virtuel, utiliser le code suivant:
* ```python -m venv <nom environnement>```


Une fois la création effectuée, il faut l'activer en l'executant comme suit:
* Sous OS Unix : ```source nom environnement/bin/activate``` 
* Sous OS Windows: ```nom environnement/Scripts/activate.bat```

Après création, nous pouvons procéder à l'installation des différents modules nécessaire pour l'execution de notre code

## 2) Installation des modules requis
Pour le bon fonctionnement du code d'application, il est nécessaire d'installer l'ensemble des modules requis, pour ce faire, il est possible d'utiliser le fichier requirements.txt et installer l'ensemble des modules indiqués dedans de la façon suivante:

```pip install -r requirements.txt```

Une fois tous les modules installés, nous pouvons procéder à l'execution du code


## Execution et fonctionnement du code
Le code de scraping est divisé en 2 modules distincts en 2 fichiers séparés : book.py et main.py

L'objectif du code est de parcourir le site web https://books.toscrape.com/ et d'en extraire un certains nombre de données

* Le module book.py va extraire les données d'un seul livre

* Le module main.py va extraire les données de l'ensemble des livre du site

-L'execution du module book.py s'effectue de la façon suivante:
```python3 book.py --url "https://singlebookurl.com"```
A renseigner en paramètre l'url d'un seul livre (ici https://singlebookurl.com)

-L'execution du module main.py, s'effectue tout simplement lancant le fichier script et celui-ci procedera à l'extraction des données de tous les livres du site https://books.toscrape.com

## Auteur
Ali HASSANE 

## Remerciements
Mon mentor Pierre-Emmanuel BRIAND, le groupe Discord Openclassrooms ainsi que l'ensemble des contributeurs des différents ressources disponible en libre accès sur le web