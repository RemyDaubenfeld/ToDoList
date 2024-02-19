# programme principal

import datetime

# connexion à la base de donnée
import mysql.connector

# Paramètres de connexion à la base de données MySQL
config = {
    'user' : 'root',
    'password' : '',
    'host' : 'localhost', #127.0.0.1
    'database' : 'pydo'
}

#connexion à la base de données
mydb = mysql.connector.connect(**config)

# initialisation d'un curseur
mycursor = mydb.cursor(dictionary=True)

# création des tables dans la base de donnée
mycursor.execute(f"CREATE TABLE IF NOT EXISTS etat(id_etat INT AUTO_INCREMENT,nom_etat VARCHAR(10),PRIMARY KEY(id_etat),UNIQUE(nom_etat));")
mycursor.execute(f"CREATE TABLE IF NOT EXISTS tache(id_tache INT AUTO_INCREMENT,nom_tache VARCHAR(100) NOT NULL,date_de_creation DATE NOT NULL,date_objectif DATE, date_de_realisation DATE, id_etat INT NOT NULL,PRIMARY KEY(id_tache),FOREIGN KEY(id_etat) REFERENCES etat(id_etat));")
mycursor.execute(f"INSERT IGNORE INTO etat (nom_etat) VALUES ('À faire'),('En cours'),('Terminée');")


# Affichage de la to do list en cours
def to_do_list():
    print("\nTo Do List de Rémy DAUBENFELD (trié par ordre d'importance)\n")
    print("\n  ETAT   |             TACHE              |     DATE CREATION    |         DATE OBJECTIF        |     DATE REALISATION")
    mycursor.execute("SELECT RPAD(nom_tache, 30,' ') AS nom_tache, date_de_creation, date_objectif, date_de_realisation, RPAD(nom_etat, 8 , ' ') AS nom_etat FROM tache RIGHT JOIN etat ON tache.id_etat = etat.id_etat WHERE nom_tache IS NOT NULL ORDER BY date_objectif;")
    list = mycursor.fetchall()
    for entry in list:
        print(f"{entry['nom_etat']} | {entry['nom_tache']} | Créé le : {entry['date_de_creation']} | A faire pour le : {entry['date_objectif']} | Terminée le {entry['date_de_realisation']}")

# Affichage du menu de la to do list
def menu():
    try:
        menu = int(input("\nQue voulez vous faire?\n1. Ajouter une nouvelle tâche\n2. Démarrer une tâche\n3. Modifier une tâche existante\n4. Finaliser une tâche\n5. Supprimer une tâche\n6. Quitter le programme\n\nVotre choix : "))
        if menu == 1:
            add_task()
        elif menu == 2:
            start_task()
        elif menu == 3:
            edit_task()
        elif menu == 4:
            complete_task()
        elif menu == 5:
            delete_task()
        elif menu == 6:
            quit()
        else:            
            print("\nVotre saisie est invalide. SVP RECOMMENCEZ !")
    except ValueError:
        print("\nVotre saisie est invalide. SVP RECOMMENCEZ !")


# Ajouter une tâche (saisie du nom de la tâche, récupération de la date du jour de la création, récupération de la date objectif)
def add_task():
    print("\n\nAJOUTER UNE NOUVELLE TACHE")
    task = input("\nVeuillez saisir le nom de la tâche à ajouter : ")
    escaped_task = task.replace("'", "''").replace("$", "\$")
    creation_date = date_creation_task()
    set_date = target_date()
    id_task = "1"
    query = f"INSERT INTO tache (nom_tache, date_de_creation, date_objectif, id_etat ) VALUES ('{escaped_task}', '{creation_date}', '{set_date}', '{id_task}')"
    mycursor.execute(query)
    mydb.commit()
    print(f"\nLa tâche '{task}' a été ajouté avec succès.\n")
    return_menu()

# Récupération de la date du jour de la création de la tâche
def date_creation_task():
    date_today = datetime.datetime.today()
    return date_today

# Saisie de la date objectif et vérification de la saisie au bon format et que la date ne soit pas antérieur à la date du jour
def target_date(): 
    while True:
        target_date = input("Veuillez saisir la date d'objectif au format AAAA-MM-DD : ")
        try:
            check_target_date = datetime.datetime.strptime(target_date, '%Y-%m-%d')
            if check_target_date >= datetime.datetime.today():
                return check_target_date
            else:
                print("\nVotre date objectif ne peut-être antérieur à la date du jour !!!")
        except ValueError:
            print("\nFormat de date invalide !!!")


# Démarrer une tâche (passage de l'état "à faire" à "en cours")
def start_task():
    print("\n\nDEMARRER UNE TACHE\n")
    # affiche la liste des taches "à faire"
    mycursor.execute("SELECT id_tache, nom_tache FROM tache RIGHT JOIN etat ON tache.id_etat = etat.id_etat WHERE etat.id_etat = 1 ORDER BY id_tache;")
    list = mycursor.fetchall()
    for entry in list:
        print(f"{entry['id_tache']} : {entry['nom_tache']}")
    print()
    # récupération des id des taches 'a faire'
    id_list = [element['id_tache'] for element in list] 
    while True:
        try:
            id_start_task = int(input("Veuillez sélectionner le numéro de la tache à démarrer : "))
            if id_start_task in id_list:
                mycursor.execute(f"UPDATE tache SET tache.id_etat = '2' WHERE id_tache = {id_start_task}")
                mydb.commit()
                mycursor.execute(f"SELECT nom_tache FROM tache WHERE id_tache = {id_start_task}")
                task_name = mycursor.fetchone()['nom_tache']
                print(f"\nLa tâche '{task_name}' est passé de l'état 'à faire' à l'état 'en cours'.")
                return_menu()
            else:
                print("\nLe numéro de tâche que vous avez choisi ne fait pas parti des tâches à démarrer.")
        except ValueError:
            print("Votre saisi est invalide !")


# Modifier une tâche
def edit_task():
    print("\n\nMODIFIER UNE TACHE\n")
    # affiche la liste des taches pouvant être modifier
    mycursor.execute("SELECT id_tache, nom_tache FROM tache WHERE tache.id_etat = 1 OR tache.id_etat = 2 AND nom_tache IS NOT NULL ORDER BY id_tache;")
    list = mycursor.fetchall()
    for entry in list:
        print(f"{entry['id_tache']} : {entry['nom_tache']}")
    print()
    # récupération des id des taches
    id_list = [element['id_tache'] for element in list] 
    while True:
        try:
            id_edit_task = int(input("Veuillez sélectionner le numéro de la tâche à modifier : "))
            if id_edit_task in id_list:
                mycursor.execute(f"SELECT nom_tache, date_objectif, etat.id_etat FROM tache RIGHT JOIN etat ON tache.id_etat = etat.id_etat WHERE id_tache = {id_edit_task}")
                task_name = mycursor.fetchone()['nom_tache']
                edit_name = 0
                while True:
                    try:
                        edit_name = int(input(f"\nVoulez-vous modifier le nom de la tâche '{task_name}'?\n1. Oui\n2. Non\nVotre choix? : "))
                        if edit_name == 1:
                            new_name = input("\nVeuillez saisir le nouveau nom de la tâche : ")
                            mycursor.execute(f"UPDATE tache SET nom_tache = '{new_name}' WHERE id_tache = {id_edit_task}")
                            mydb.commit()
                            print(f"\nLe nom de la tache '{task_name}' a été modifié par '{new_name}'.")
                            break
                        elif edit_name == 2:
                            break
                        else : 
                            print("\nVotre saisi est invalide !") 
                    except ValueError:
                        print("\nVotre saisi est invalide !")
                mycursor.execute(f"SELECT nom_tache, date_objectif, etat.id_etat FROM tache RIGHT JOIN etat ON tache.id_etat = etat.id_etat WHERE id_tache = {id_edit_task}")
                task_set_date = mycursor.fetchone()['date_objectif']
                edit_set_date = 0
                while True:
                    try:
                        edit_set_date = int(input(f"\nVoulez-vous modifier la date d'objectif de la tâche '{task_name}'?\n1. Oui\n2. Non\nVotre choix? :  "))
                        if edit_set_date == 1:
                            new_set_date = target_date()
                            mycursor.execute(f"UPDATE tache SET date_objectif = '{new_set_date}' WHERE id_tache = {id_edit_task}")
                            mydb.commit()
                            print(f"La date objectif du '{task_set_date} a été modifié par la date du '{new_set_date}'.")
                            break
                        elif edit_set_date == 2:
                            break
                    except ValueError:
                        print("\nVotre saisi est invalide !")
                mycursor.execute(f"SELECT nom_tache, date_objectif, tache.id_etat AS tache FROM tache RIGHT JOIN etat ON tache.id_etat = etat.id_etat WHERE id_tache = {id_edit_task}")
                id_state_task = mycursor.fetchone()['tache']
                while True:
                    try:
                        if id_state_task == 2:
                            while True:
                                try:
                                    edit_id = int(input(f"\nVoulez-vous faire retourner votre tâche de l'état 'en cours' à l'état 'à faire'?\n1. Oui\n2. Non\nVotre choix : "))
                                    if edit_id == 1:
                                        mycursor.execute(f"UPDATE tache SET id_etat = '1' WHERE id_tache = {id_edit_task}")
                                        mydb.commit()
                                        print(f"\nL'état de la tache est passé de 'en cours' à 'à faire'.")
                                        break
                                    elif edit_id == 2:
                                        break
                                    else:
                                        print("\nVotre saisi est invalide !")
                                    break
                                except ValueError:
                                    print("\nVotre saisi est invalide !")
                        else : 
                            break
                    except ValueError:
                        print("\nVotre saisi est invalide !")
            else :
                print("\nLe numéro de tâche que vous avez choisi ne fait pas parti des tâches pouvant être modifier.")
            break
        except ValueError:
            print("\nVotre saisi est invalide !")
            
        
# Finaliser une tâche et enregistrement de la date de réalisation
def complete_task():
    print("\n\nTERMINER UNE TACHE\n")
    # affiche la liste des taches "à faire" et "en cours"
    mycursor.execute("SELECT id_tache, nom_tache FROM tache RIGHT JOIN etat ON tache.id_etat = etat.id_etat WHERE etat.id_etat = 1 OR etat.id_etat = 2 ORDER BY id_tache;")
    list = mycursor.fetchall()
    for entry in list:
        print(f"{entry['id_tache']} : {entry['nom_tache']}")
    print()
    # récupération des id des taches
    id_list = [element['id_tache'] for element in list] 
    while True:
        try:
            id_finish_task = int(input("Veuillez sélectionner le numéro de la tache à terminer : "))
            if id_finish_task in id_list:
                mycursor.execute(f"UPDATE tache SET tache.id_etat = '3' WHERE id_tache = {id_finish_task}")
                mydb.commit()
                break
            else:
                print("\nLe numéro de tâche que vous avez choisi ne fait pas parti des tâches à terminer.")
        except ValueError:
            print("Votre saisi est invalide !")
    completion_date = finish_date()
    mycursor.execute(f"UPDATE tache SET date_de_realisation = '{completion_date}' WHERE id_tache = {id_finish_task}")
    mydb.commit()
    mycursor.execute(f"SELECT nom_tache FROM tache WHERE id_tache = {id_finish_task}")
    task_name = mycursor.fetchone()['nom_tache']
    print(f"\nFélicitation, la tâche '{task_name}' est maintenant 'terminée'.")
    return_menu()

# Saisie de la date de finalisation et vérification par rapport à la date de création
def finish_date(): 
    while True:
        finish_date = input("Veuillez saisir la date de finalisation de la tâche au format AAAA-MM-DD : ")
        try:
            check_finish_date = datetime.datetime.strptime(finish_date, '%Y-%m-%d')
            if check_finish_date >= date_creation_task():
                return check_finish_date
            else:
                print("\nVotre date de fin ne peut-être antérieur à la date de création de la tâche !!!")
        except ValueError:
            print("\nFormat de date invalide !!!")


# Suppression d'une tâche et confirmation de la suppression
def delete_task():
    print("\n\nSUPPRIMER UNE TACHE\n")
    # affiche la liste de toutes les taches
    mycursor.execute("SELECT id_tache, nom_tache FROM tache RIGHT JOIN etat ON tache.id_etat = etat.id_etat ORDER BY id_tache;")
    list = mycursor.fetchall()
    for entry in list:
        print(f"{entry['id_tache']} : {entry['nom_tache']}")
    print()
    # récupération des id des taches
    id_list = [element['id_tache'] for element in list] 
    while True:
        try:
            id_delete_task = int(input("Veuillez sélectionner le numéro de la tache à supprimer : "))
            if id_delete_task in id_list:
                # demande de confirmation de la supression
                while True:
                    try:
                        deletion_confirmation = int(input("\nEtes-vous sûre de vouloir supprimer cette tâche?\n1. Oui\n2. Non\n3. Retour au menu principal\nVotre choix : "))
                        if deletion_confirmation == 1:
                            mycursor.execute(f"SELECT nom_tache FROM tache WHERE id_tache = {id_delete_task}")
                            task_name = mycursor.fetchone()['nom_tache']
                            mycursor.execute(f"DELETE FROM tache WHERE id_tache = {id_delete_task}")
                            mydb.commit()
                            print(f"\nLa tâche '{task_name}' a été supprimé !")
                            return_menu()
                        elif deletion_confirmation == 2:
                            print("\nRetour au menu de suppression")
                            delete_task()
                        elif deletion_confirmation == 3:
                            to_do_list()
                            menu()
                        else:
                            print("\nVotre saisi est invalide !")
                    except ValueError:
                        print("Votre saisi est invalide !")
            else:
                print("\nLe numéro de tâche que vous avez choisi ne fait pas parti des tâches à supprimer.")
        except ValueError:
            print("Votre saisi est invalide !")
    

def return_menu():
    while True:
        try:
            end_program = int(input("\nSouhaitez vous revenir au menu principal ou fermer le programme?\n1. Menu principal\n2. Fermer le programme\nVotre choix : "))
            if end_program == 1:
                to_do_list()
                menu()
            elif end_program == 2:
                quit()
            else:
                print("\nVotre saisi est invalide !")
        except ValueError:
            print("Votre saisi est invalide !")
            

# execution du programme
to_do_list() 
menu()
return_menu()
# les choix dans le menu renvois vers des fonctions et un choix à la fin du programme de chaque fonction permet de revenir vers le menu ou de quitter