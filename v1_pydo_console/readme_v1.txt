TOUT_DOUX_LISTE version 1


Le programme fonctionne avec Python et une base de donnée MySQL.

Avant de lancer le programme tout_doux_liste.py pour la première fois, veuillez vous assurez que vous avez Python d'installer sur votre ordinateur et que votre logiciel VSCode possède le module mysql.connector pour se connecter à la base de donnée.


Si vous n'avez pas Python installer sur votre ordinateur, vous pouvez le télécharger via ce lien: https://www.python.org/downloads/. Lors de l'installation, cocher les 2 cases en bas de la fenêtre pour ajouter le dossier du logiciel dans le Path.


Voici le modules de VSCode qui doit être installer : (la commande est à taper dans le terminale de commande du logiciel ou directement depuis l'invite de commande windows)

- MySql.connector (pour la connexion à la base de donnée) : pip install mysql-connector-python


Une fois ces prérequis installé, voici les étapes :

1. Lancer votre Wampserver

2. Connectez vous à PhpMyAdmin avec les identifiants suivants
   - Utilisateur : root
   - Mot de passe :
   - Choix du serveur : MySQL

3. Créez la base de données
   - Nom de la base de donnée : pydo
   - Jeu de caractères : utf8mb4_general_ci

4. Lancer tout_doux_liste.py

Les tables seront créé automatiquement dans la base de donnée lors du lancement du programme.