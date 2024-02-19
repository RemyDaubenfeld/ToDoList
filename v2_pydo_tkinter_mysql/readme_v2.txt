TOUT_DOUX_LISTE version 2


Le programme fonctionne avec Python, des modules Pythons(dont tkinter pour l'interface graphique) et une base de donnée MySQL. 

Avant de lancer le programme tout_doux_liste.pyw pour la première fois, veuillez vous assurez que vous avez Python d'installer sur votre ordinateur et que votre logiciel VSCode possède les modules python nécessaire.


Si vous n'avez pas Python installer sur votre ordinateur, vous pouvez le télécharger via ce lien: https://www.python.org/downloads/. Lors de l'installation, cocher les 2 cases en bas de la fenêtre pour ajouter le dossier du logiciel dans le Path.


Voici les modules de VSCode qui doivent être installer : (les commandes sont à taper dans le terminale de commande du logiciel ou directement depuis l'invite de commande windows)

- Tkinter (pour l'interface graphique): pip install tk
- Pillow (pour la gestion des images du programme) : pip install pillow
- Tkcalendar (pour l'intégration des calendriers) : pip install tkcalendar
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

4. Lancer tout_doux_liste.pyw

Les tables seront créé automatiquement dans la base de donnée lors du lancement du programme.