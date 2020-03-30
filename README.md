# PROJ831 - Database and use project

## Subject (in french) :

Je vous ai envoyé, via la plateforme d’envoi de fichiers volumineux, un fichier type de log à traiter.

Dans un premier temps, je vous conseille de ne regarder que les logs de [WGraph ...] concernant l’exécution d'une transition ("try to run edge" et "edge runned"). Les WGraph sont des graphes État/Transition, chaque objet domotique a son propre graphe, les log suscité son les enregistrement des changements d'états des graphes.

Via les log, vous n'avez aucune information de corrélation entre les graphes.

Les log, vous sont données sous forme de fichier, mais il peuvent accessible via d'autres flux (MQTT, BD...), il faudra donc en tenir compte dans la réalisation du projet.

Comme vous êtes nombreux, il faudra prévoir dans le projet, en plus de la gestion de projet, une partie analyse (recherche de modèle de comportement de chaque graphe, corrélation entre les comportements, prédiction de comportement, écart au modèle...), une partie visualisation afin d'avoir une vue conviviale, originale, mais surtout pertinente des données de log et d'analyse, et enfin la partie infrastructure qui doit faire le lien entre l'acquisition des données, l'analyse et la visualisation.

La seule contrainte que vous ayez, sauf si le module en impose d'autres, est d'utiliser des langages/bibliothèques/applications fiables et pérennes.

## Dependencies :

* python 3.X (tested with python 3.7.4 with or without Anaconda 3)
* python packages :
  * Flask (https://flask.palletsprojects.com/en/1.1.x/installation/#installation)
  * pymongo (https://pymongo.readthedocs.io/en/stable/installation.html)
* MongoDB (https://www.mongodb.com/community)

## Instructions :
**To start the web server :**

1. Install Flask
`pip install Flask`


2. Add the application as env var:
  * (Windows PowerShell): `$env:FLASK_APP = "Dashboard/application.py`
  * (Linux): `export FLASK_APP=Dashboard/application.py`


3. Run the server:
`flask run`
