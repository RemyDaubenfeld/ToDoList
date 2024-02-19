# programme principal

# region : IMPORTS

from datetime import datetime
from datetime import date
import mysql.connector
import webbrowser

from tkinter import ttk
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# endregion : IMPORTS


# region : CONNECTION A LA BASE DE DONNEES

# Paramètres de connexion à la base de données MySQL
def database():
        config = {
            'user' : 'root',
            'password' : '',
            'host' : 'localhost', #127.0.0.1
            'database' : 'pydo'
        }
        global mydb 
        mydb = mysql.connector.connect(**config)
        mydb.autocommit = True  # Activation de l'auto-commit
        global mycursor

        # initialisation de la base de donnée
        mycursor= mydb.cursor(dictionary=True)

        # construction des tables dans la base de donnée
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS etat(id_etat INT AUTO_INCREMENT,nom_etat VARCHAR(10),PRIMARY KEY(id_etat),UNIQUE(nom_etat));")
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS tache(id_tache INT AUTO_INCREMENT,nom_tache VARCHAR(100) NOT NULL,date_de_creation DATE NOT NULL,date_objectif DATE, date_de_realisation DATE, id_etat INT NOT NULL,PRIMARY KEY(id_tache),FOREIGN KEY(id_etat) REFERENCES etat(id_etat));")
        mycursor.execute(f"INSERT IGNORE INTO etat (nom_etat) VALUES ('À faire'),('En cours'),('Terminée');")

# endregion : CONNECTION A LA BASE DE DONNEES


# region : COULEUR ET FONT
        
# variable de couleur utilisé pour l'interface graphique
# Background color
bg_yellow = "#f3ff90"
bg_gray = "#D3D3D3"
bg_red = "#f00020"
bg_green = "#008000"

# color
fg_white = "#ffffff"
fg_blue = '#03183A'
fg_orange = '#d35317'
fg_green = "#008000"

#font
font = "verdana"

# endregion : COULEUR ET FONT


# region : LIEN HYPERTEXTE
def github(event):
    url = "https://github.com/RemyDaubenfeld"
    webbrowser.open(url)

def linkedin(event):
    url = "https://www.linkedin.com/in/remydaubenfeld"
    webbrowser.open(url)

# endregion : LIEN HYPERTEXTE


# region : FENETRE PRINCIPALE

# Import du logo
def logo():
    # Charger l'image, réduire la taille et convertir
    image_filename = "img/logo.png"
    original_img = Image.open(image_filename)
    resized_img = original_img.copy()
    resized_img.thumbnail((90, 90))
    img = ImageTk.PhotoImage(resized_img)
    # Créer un Label pour afficher l'image
    photo_label = tk.Label(frame, image=img)
    photo_label.image = img
    photo_label.pack(side=tk.LEFT, padx=30)
    
# Changement du logo et du titre des fenêtres
def window_icon(window, window_title):
    display_list.iconphoto(True, tk.PhotoImage(file = "img/logo.png"))
    window.title(window_title)

# Initialisation de la fenêtre et de la couleur
def window_app():
    global display_list
    display_list = Tk() # création de l'objet-fenêtre graphique
    display_list.configure(bg=bg_yellow)
    display_list.resizable(width=False, height=False)

    window_icon(display_list, "TOUT DOUX LISTE : La liste pour faire les tâches en douceur")
    
    # Création de la frame titre + logo
    global frame
    frame = Frame(display_list, borderwidth = 0, relief = FLAT, bg=bg_gray)
    frame.pack(fill = X)
    logo()
    title = Label(frame, text="TOUT DOUX LISTE\nLa liste pour faire les tâches en douceur", font=(font,20), pady = 30, bg=bg_gray)
    title.pack(side=tk.LEFT)

    frame_list = Frame(display_list, borderwidth = 0, relief = FLAT, bg=bg_yellow) 
    frame_list.pack()

    refresh_photo = PhotoImage(file="img/refresh.png")
    refresh_task_button = Button(frame_list, image = refresh_photo, relief = FLAT, bg = bg_yellow, cursor="tcross", width = 15, bd = 0, activebackground = bg_yellow)
    refresh_task_button.image = refresh_photo
    refresh_task_button.bind("<Button-1>", lambda event: update_table(event))
    refresh_task_button.pack(side=LEFT, fill="both", expand=True, padx=10) 

    name_list = Label(frame_list, text="Liste des choses à faire", font=20, pady = 10, bg=bg_yellow)
    name_list.pack(side=LEFT, fill="both", expand=True, padx=10)

    treeview()
    
    menu()

    frame_footer = Frame(display_list, borderwidth = 0, relief=FLAT, bg=bg_gray)
    frame_footer.pack(side=BOTTOM, fill = X)
    photo_footer = PhotoImage(file="img/footer_logo.png")
    title_footer = Label(frame_footer, text="by Rémy DAUBENFELD", image = photo_footer, compound ="right", font=(font, 10), bg=bg_gray)
    title_footer.image = photo_footer
    title_footer.pack(side=LEFT, expand=TRUE, pady=5) 

      
    logo_linkedin = PhotoImage(file="img/linkedin.png")
    linkedin_button = Button(frame_footer, image = logo_linkedin, relief = FLAT, cursor="tcross")
    linkedin_button.image = logo_linkedin
    linkedin_button.bind("<Button-1>", linkedin)
    linkedin_button.pack(side=RIGHT, padx=10)

    logo_github = PhotoImage(file="img/github.png")
    github_button = Button(frame_footer, image = logo_github, relief = FLAT, cursor="tcross")
    github_button.image = logo_github
    github_button.bind("<Button-1>", github)
    github_button.pack(side=RIGHT, padx=10)

# Affichage du menu de la to do list
def menu():
    frame_button = Frame(display_list, borderwidth = 0, relief = FLAT, bg=bg_yellow) 
    frame_button.pack(fill=X)

    # Ajout des bouttons du menu
    add_photo = PhotoImage(file="img/add.png")
    add_task_button = Button(frame_button, text = "Ajouter", image = add_photo, compound ="left", relief = FLAT, bg = bg_green, fg = fg_white, cursor="tcross", width = 100, height = 20, bd = 0, activebackground = bg_green)
    add_task_button.image = add_photo
    add_task_button.bind("<Button-1>", add_task_window)
    add_task_button.pack(side=tk.LEFT, pady=20, expand=True)
    
    edit_photo = PhotoImage(file="img/edit.png")
    edit_task_button = Button(frame_button, text = "Editer", image = edit_photo, compound ="left", relief = FLAT, bg = bg_gray, cursor="tcross", width = 100, height = 20, bd = 0, activebackground=bg_gray)
    edit_task_button.image = edit_photo
    edit_task_button.bind("<Button-1>", edit_task_window)
    edit_task_button.pack(side=tk.LEFT, pady=20, expand=True)
    
    start_photo = PhotoImage(file="img/start.png")
    start_task_button = Button(frame_button, text = "Débuter", image = start_photo, compound ="left", relief = FLAT, bg = bg_gray, cursor="tcross", width = 100, height = 20, bd = 0, activebackground=bg_gray)
    start_task_button.image = start_photo
    start_task_button.bind("<Button-1>", start_task_window)
    start_task_button.pack(side=tk.LEFT, pady=20, expand=True)
    
    complete_photo = PhotoImage(file="img/finish.png")
    complete_task_button = Button(frame_button, text = "Finaliser", image = complete_photo, compound ="left", relief = FLAT, bg = bg_gray, cursor="tcross", width = 100, height = 20, bd = 0, activebackground=bg_gray)
    complete_task_button.image = complete_photo
    complete_task_button.bind("<Button-1>", complete_task_window)
    complete_task_button.pack(side=tk.LEFT, pady=20, expand=True)
    
    delete_photo = PhotoImage(file="img/delete.png")
    delete_task_button = Button(frame_button, text = "Supprimer", image=delete_photo, compound ="left", relief = FLAT, bg = bg_red, fg = fg_white, cursor="tcross", width = 100, height = 20, bd = 0, activebackground=bg_red)
    delete_task_button.image = delete_photo
    delete_task_button.bind("<Button-1>", delete_task_window)
    delete_task_button.pack(side=tk.LEFT, pady=20, expand=True)

# endregion : FENETRE PRINCIPALE


# region : LISTE DES TACHES

# Création du tableau avec importation de la "to do list"
def treeview ():
    global frame_treeview
    frame_treeview = Frame(display_list, borderwidth = 0, relief = FLAT, bg=bg_yellow) 
    frame_treeview.pack()

    global table
    table = ttk.Treeview(frame_treeview)    
    
    table["columns"] = ("Etat", "Tâche", "Créé le", "A faire pour le", "Temps restant", "Réalisé le")
    
    # Définition des en-têtes  et des tailles de colonne
    table.column("#0", width=0, anchor=CENTER, stretch=NO)
    table.heading("Etat", text="Etat", command=lambda: sort_column(table, "Etat"))
    table.column("Etat", width=80, anchor=CENTER, minwidth = 80)
    
    table.heading("Tâche", text="Tâche", command=lambda: sort_column(table, "Tâche"))
    table.column("Tâche", width=200, anchor=CENTER, minwidth = 200)
    
    table.heading("Créé le", text="Créé le", command=lambda: sort_column(table, "Créé le"))
    table.column("Créé le", width=100, anchor=CENTER, minwidth = 100)
    
    table.heading("A faire pour le", text="A faire pour le", command=lambda: sort_column(table, "A faire pour le"))
    table.column("A faire pour le", width=100, anchor=CENTER, minwidth = 100)

    table.heading("Temps restant", text="Temps restant", command=lambda: sort_column(table, "Temps restant"))
    table.column("Temps restant", width=100, anchor=CENTER, minwidth = 100)
    
    table.heading("Réalisé le", text="Réalisé le", command=lambda: sort_column(table, "Réalisé le"))
    table.column("Réalisé le", width=100, anchor=CENTER, minwidth = 100)

    to_do_list(table)


# Possibilité de trier par colonne 
def sort_column(tree, col, reverse = False):
    sorting = [(tree.set(k, col), k) for k in tree.get_children('')]
    sorting.sort(reverse=reverse)
    for index, (val, k) in enumerate(sorting):
        tree.move(k, '', index)
    tree.heading(col, command = lambda: sort_column(tree, col, not reverse))


# Création de la scrollbar
def create_scrollbar(frame_treeview, table):
    # Hauteur maximale du tableau
    max_table_height = 15

    # Vérifier si une barre de défilement existe déjà
    existing_scrollbar = frame_treeview.children.get("y_scrollbar")
    
    # Si le tableau dépasse 15 lignes, ajouter une scrollbar
    if len(table.get_children()) > max_table_height:
        # Si une barre de défilement n'existe pas, ou si elle a été détruite, créer une nouvelle
        if not existing_scrollbar:
            y_scrollbar = Scrollbar(frame_treeview, orient=VERTICAL, command=table.yview, name="y_scrollbar")
            y_scrollbar.pack(side=RIGHT, fill=Y)
            table.configure(height=max_table_height, yscrollcommand=y_scrollbar.set)
            table.pack(side=LEFT)
            
    # Si le tableau fait moins de 15 lignes, ajuster la hauteur du tableau et détruire la barre de défilement
    else:
        # Si une barre de défilement existe, la détruire
        if existing_scrollbar:
            existing_scrollbar.destroy()
            table.pack()
        # Ajuster la hauteur du tableau
        table.configure(height=len(table.get_children()))
        table.pack()


def get_state_color(state):
    color_mapping = {
        'À faire': fg_blue,
        'En cours': fg_orange,
        'Terminée': fg_green,
        
    }
    return color_mapping.get(state, 'black')


# Affichage de la to do list en cours dans le tableau
def to_do_list(table):
    mycursor.execute("SELECT nom_tache, date_de_creation, date_objectif, date_de_realisation, nom_etat FROM tache RIGHT JOIN etat ON tache.id_etat = etat.id_etat WHERE nom_tache IS NOT NULL ORDER BY date_objectif;")
    list = mycursor.fetchall()

     # Configurer les tags avant d'insérer les données
    for state in ['À faire', 'En cours', 'Terminée']:
        state_color = get_state_color(state)
        table.tag_configure(state, foreground=state_color)

    if mycursor.rowcount > 0:
        for entry in list:
            # Calcul du temps restant
            temps_restant = ''
            if entry['date_de_realisation']:
                temps_restant = ""
            else:
                temps_restant = entry['date_objectif'] - date.today()
                if 'Terminée' != None and temps_restant.days >= 0:
                    temps_restant = f"{(entry['date_objectif'] - date.today()).days} jour(s)"
                else:
                    temps_restant = "Dépassée"
            # Formatage des dates au format dd-mm-yyyy
            creation_date_formatted = entry['date_de_creation'].strftime('%d-%m-%Y')
            set_date_formatted = entry['date_objectif'].strftime('%d-%m-%Y')
            finish_date_formatted = entry['date_de_realisation'].strftime('%d-%m-%Y') if entry['date_de_realisation'] else ""
            # Insertion des données dans le tableau
            row_id = table.insert("", "end", values=(
                f"{entry['nom_etat']}", 
                f"{entry['nom_tache']}",
                creation_date_formatted,
                set_date_formatted,
                temps_restant,
                finish_date_formatted if entry['date_de_realisation'] else ""
            ))

            # Appliquer le tag en fonction du statut de la tâche
            table.item(row_id, tags=(entry['nom_etat'],))

        create_scrollbar(frame_treeview, table)
    else:
        messagebox.showinfo("Information", "Aucune tâche trouvée dans la base de données.")

# Mise à jour de la liste des tâches
def update_table(event):
    # Supprimer toutes les lignes existantes dans le tableau
    table.delete(*table.get_children())
    # Réinsérer les données mises à jour
    to_do_list(table)

# endregion : LISTE DES TACHES


# region : NOUVELLE FENETRE ET FERMETURE FENETRE

# Création des fenêtres(adapter le paramêtre avec le nom de la fenêtre)
def new_window(name_window):
    new_window = Toplevel(display_list)
    new_window.configure(bg=bg_yellow)
    new_window.resizable(width=False, height=False)

    window_width = 700
    window_height = 320
    new_window.geometry(f"{window_width}x{window_height}")
    
    window_icon(new_window, name_window)
    frame_add = Frame(new_window, relief = FLAT, bg=bg_gray)
    frame_add.pack(fill = X)
    title_add = Label(frame_add, text= name_window, font=(font,20), pady = 30, bg=bg_gray)
    title_add.pack()

    return new_window

# Fermeture de fenêtre
def close_window(window_name):
    window_name.destroy()

# endregion : NOUVELLE FENETRE ET FERMETURE FENETRE


# region : AJOUTER UNE TACHE

# Fenêtre "ajouter une tâche"
def add_task_window(event):
    global add_task_wind
    add_task_wind = new_window("Ajouter une tâche")
    
    name_task_frame = Frame(add_task_wind, bg=bg_yellow)
    name_task_frame.pack(fill=X)

    label_task = Label(name_task_frame, text = "Nom de la tâche à ajouter :",font = (font, 10) ,bg=bg_yellow)
    label_task.pack(side=LEFT, expand=True, padx=10, pady=15)

    global input_task
    input_task = Entry(name_task_frame, bd = 1, width = 80, font = (font, 10))
    input_task.pack(side=LEFT, padx=10, pady=15)


    date_task_frame = Frame(add_task_wind, bg=bg_yellow)
    date_task_frame.pack(fill=X)

    label_target_date = Label(date_task_frame, text = "Date d'objectif:",font = (font, 10), bg=bg_yellow)
    label_target_date.pack(side=LEFT ,padx=10, pady=15)
    
    global input_target_date
    input_target_date = DateEntry(date_task_frame, bd = 1, font = (font, 10), date_pattern='dd-mm-yyyy')
    input_target_date.pack(side=LEFT, padx=10, pady=15)

    validate_photo = PhotoImage(file="img/add.png")
    validate_button = Button(add_task_wind, text = "Ajouter", image = validate_photo, compound ="left", relief = FLAT,  bg = bg_green, fg = fg_white, cursor="tcross", width = 100, height = 20, bd = 0, activebackground = bg_green)
    validate_button.image = validate_photo
    validate_button.bind("<Button-1>", add_task)
    validate_button.pack(side=tk.LEFT, padx=10, expand=True)

    quit_photo = PhotoImage(file="img/quit.png")
    quit_button = Button(add_task_wind, text = "Fermer", image = quit_photo, compound ="left", relief = FLAT, bg = bg_red, fg = fg_white, cursor="tcross", width = 100, height = 20, bd = 0, activebackground = bg_red)
    quit_button.image = quit_photo
    quit_button.bind("<Button-1>", lambda event=None: close_window(add_task_wind))
    quit_button.pack(side=tk.LEFT, padx=10, expand=True)

    #liaison de la touche "entrer" à la command "add_task"
    input_task.bind("<Return>", add_task)    

# Ajouter une tâche (récupération du nom de la tâche et de la date et vérification des conditions rempli pour exécuter la reqûete)
def add_task (event):
    escaped_task = input_task.get()
    escaped_task = escaped_task.replace("'", "''")

    creation_date = date.today()
    set_date = input_target_date.get_date() if input_target_date.get() else None
    id_task = "1"
    while True:
        try:
            if set_date >= creation_date and escaped_task != '':
                mycursor.execute(f"INSERT INTO tache (nom_tache, date_de_creation, date_objectif, id_etat) VALUES "f"('{escaped_task}', '{creation_date}', '{set_date}', '{id_task}')")
                add_task_wind.destroy()
                break
            elif set_date < creation_date:
                messagebox.showwarning("Avertissement", "La date d'objectif ne peut pas être antérieure à la date de création de la tâche.")
                add_task_wind.deiconify() #Retour à la fenêtre 
                break
            elif escaped_task == '':
                messagebox.showwarning("Avertissement", "Veuillez entrer une tâche.")
                add_task_wind.deiconify()
                break
        except:
            messagebox.showwarning("Erreur", "Veuillez entrer une tâche ou une date d'objectif.")
            add_task_wind.deiconify()
            break
    update_table(event)

# endregion : AJOUTER UNE TACHE


# region : MODIFIER UNE TACHE
    
def edit_task_window(event):
    global selected_edit_item
    selected_edit_item = table.selection()
    if selected_edit_item:
        global selected_edit_task_values
        selected_edit_task_values = table.item(selected_edit_item) ["values"]

        # Requête pour obtenir l'id_tache en fonction du nom de la tâche
        mycursor.execute(f"SELECT id_tache, id_etat, date_objectif FROM tache WHERE nom_tache = %s", (selected_edit_task_values[1],))
        global edit_query_result
        edit_query_result = mycursor.fetchone()
        
        if edit_query_result:
            global edit_id_task
            edit_id_task = edit_query_result.get('id_tache')
            global edit_id_state
            edit_id_state = edit_query_result.get('id_etat')
        
        global edit_task_wind
        edit_task_wind = new_window("Modifier une tâche")

        # Libellé des colonnes
        frame_column = Frame(edit_task_wind, bg = bg_yellow, pady= 10)
        frame_column.pack(side=TOP, fill=X)

        label_state_task = Label(frame_column, text="CHANGER ETAT", bg=bg_yellow, font = (font, 10))
        label_state_task.pack(side=tk.LEFT, fill="both", expand=True)

        label_name_task = Label(frame_column, text="CHANGER NOM DE TACHE", bg=bg_yellow, font = (font, 10))
        label_name_task.pack(side=tk.LEFT, fill="both", expand=True)
        
        label_set_task = Label(frame_column, text="CHANGER DATE OBJECTIF", bg=bg_yellow, font = (font, 10))
        label_set_task.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Eléments à modifier     
        frame_old_label = Frame(edit_task_wind, pady= 5, bg = bg_yellow)
        frame_old_label.pack(side=TOP, fill=X)

        label_state_task = Label(frame_old_label, text=f"{selected_edit_task_values[0]}", font = (font, 10))
        label_state_task.pack(side=tk.LEFT, fill="both", expand=True)

        label_name_task = Label(frame_old_label, text=f"{selected_edit_task_values[1]}", font = (font, 10))
        label_name_task.pack(side=tk.LEFT, fill="both", expand=True)
        
        label_set_task = Label(frame_old_label, text=f"{selected_edit_task_values[3]}", font = (font, 10))
        label_set_task.pack(side=tk.LEFT, fill="both", expand=True)


        # Update
        frame_update = Frame(edit_task_wind, bg=bg_yellow)
        frame_update.pack(side=TOP, fill=X)
        

        frame_radiobutton = Frame(frame_update, bg=bg_yellow)
        frame_radiobutton.pack(side = LEFT, padx=40)
        global new_value
        new_value = IntVar()
        new_value.set(edit_id_state)
        bouton1 = Radiobutton(frame_radiobutton, text="A faire", variable = new_value, value = 1, bg=bg_yellow)
        bouton2 = Radiobutton(frame_radiobutton, text="En cours", variable = new_value, value = 2, bg=bg_yellow)
        bouton3 = Radiobutton(frame_radiobutton, text="Terminée", variable = new_value, value = 3, bg=bg_yellow)
        bouton1.pack()
        bouton2.pack()
        bouton3.pack()
   
        global new_input_task
        new_input_task = Entry(frame_update, bd = 1, width = 30, font = (font, 10))
        new_input_task.insert(0, selected_edit_task_values[1])  # Insérer la valeur de la tâche sélectionnée
        new_input_task.pack(side=tk.LEFT,padx=5, expand=True)

        global new_input_target_date
        new_input_target_date = DateEntry(frame_update, bd=1, font = (font, 10), date_pattern='dd-mm-yyyy')
        new_input_target_date.set_date(selected_edit_task_values[3])
        new_input_target_date.pack(side=tk.LEFT,padx=5, expand=True)


        # Boutons
        frame_button = Frame(edit_task_wind, pady= 10, bg=bg_yellow)
        frame_button.pack(side=BOTTOM, fill=X)

        validate_photo = PhotoImage(file="img/validate.png")
        validate_button = Button(frame_button, text = "Valider", image = validate_photo, compound ="left", relief = FLAT,  bg = bg_green, fg = fg_white, cursor="tcross", width = 100, height = 20, bd = 0, activebackground = bg_green)
        validate_button.image = validate_photo
        validate_button.bind("<Button-1>", validate)
        validate_button.pack(side=LEFT, padx=10, expand=True)


        quit_photo = PhotoImage(file="img/quit.png")
        quit_button = Button(frame_button, text = "Fermer", image = quit_photo, compound ="left", relief = FLAT, bg = bg_red, fg = fg_white, cursor="tcross", width = 100, height = 20, bd = 0,   activebackground = bg_red)
        quit_button.image = quit_photo
        quit_button.bind("<Button-1>", lambda event=None: close_window(edit_task_wind))
        quit_button.pack(side=LEFT, padx=10, expand=True)

    else:
        messagebox.showerror("Erreur", "Veuillez d'abord sélectionner une tâche à modifier.")

def validate(event):
    # Obtenir les nouvelles valeurs de frame_update
    new_state = new_value.get()
    new_name = new_input_task.get()
    new_target_date = new_input_target_date.get()

    # Comparer avec les valeurs de frame_old_label
    old_state = edit_id_state
    old_name = selected_edit_task_values[1]
    old_target_date = selected_edit_task_values[3]

    # Vérifier s'il y a des modifications
    if new_state != old_state or new_name != old_name or new_target_date != old_target_date:
        if new_state != old_state:
            mycursor.execute(f"UPDATE tache SET tache.id_etat = '{new_state}' WHERE id_tache = '{edit_id_task}'")
            if new_state == 3 :
                completion_date = date.today()
                mycursor.execute(f"UPDATE tache SET date_de_realisation = '{completion_date}' WHERE id_tache = '{edit_id_task}'")
            elif old_state == 3: 
                completion_date = ""
                mycursor.execute(f"UPDATE tache SET date_de_realisation = '{completion_date}' WHERE id_tache = '{edit_id_task}'")

            edit_task_wind.destroy()
        else :
            pass

        if new_name != old_name:
            new_name = new_name.replace("'", "''")
            mycursor.execute(f"UPDATE tache SET tache.nom_tache = '{new_name}' WHERE id_tache = '{edit_id_task}'")
            
            edit_task_wind.destroy()
        else :
            pass

        if new_target_date != old_target_date:
            if new_target_date < selected_edit_task_values[2]:
                messagebox.showerror("Erreur", "Vous ne pouvez sélectionner une date antérieur à la date de création de la tâche.")
                edit_task_wind.deiconify()
            else : 
                new_target_date = datetime.strptime(new_target_date, '%d-%m-%Y')
                mycursor.execute(f"UPDATE tache SET tache.date_objectif = '{new_target_date}' WHERE id_tache = '{edit_id_task}'")
                edit_task_wind.destroy()
        update_table(None)
        
    else:
        messagebox.showinfo("Information", "Aucune modification détectée.")
        edit_task_wind.deiconify()
    
# endregion : MODIFIER UNE TACHE
        

# region : DEMARRER UNE TACHE

def start_task_window(event):
    selected_item = table.selection()
    if selected_item:
        selected_task_name = table.item(selected_item)["values"][1] #Le 1 correspond à la colonne tâche
        
        # Requête pour obtenir l'id_tache en fonction du nom de la tâche
        mycursor.execute(f"SELECT id_tache, id_etat FROM tache WHERE nom_tache = %s", (selected_task_name,))
        query_result = mycursor.fetchone()

        if query_result:
            id_etat = query_result.get('id_etat')
            id_tache = query_result.get('id_tache')
            
            if id_etat == 1:
                confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir démarrer la tâche '{selected_task_name}'?")
               
                if confirmation:
                    mycursor.execute(f"UPDATE tache SET tache.id_etat = '2' WHERE id_tache = '{id_tache}'")
                   
                    update_table(event)
            elif id_etat == 2:
                messagebox.showerror("Erreur", f"La tâche '{selected_task_name}' est déjà en cours.")
            else:
                messagebox.showerror("Erreur", f"La tâche '{selected_task_name}' est déjà terminée.")
        else:
            messagebox.showerror("Erreur", "Tâche non trouvée dans la base de données")
    else :
        messagebox.showerror("Erreur", "Veuillez d'abord sélectionner une tâche à démarrer.")

# endregion : DEMARRER UNE TACHE


# region : FINALISER UNE TACHE
        
def complete_task_window(event):
    selected_item = table.selection()
    if selected_item:
        selected_task_name = table.item(selected_item)["values"][1] #Le 1 correspond à la colonne tâche
        
        # Requête pour obtenir l'id_tache en fonction du nom de la tâche
        print(selected_task_name)
        mycursor.execute(f"SELECT id_tache, id_etat FROM tache WHERE nom_tache = %s", (selected_task_name,))
        query_result = mycursor.fetchone()

        if query_result:
            id_etat = query_result.get('id_etat')
            id_tache = query_result.get('id_tache')
            
            if id_etat == 1 or id_etat == 2:
                confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir terminée la tâche '{selected_task_name}'?")
               
                if confirmation:
                    mycursor.execute(f"UPDATE tache SET tache.id_etat = '3' WHERE id_tache = '{id_tache}'")
                
                    completion_date = date.today()
                    mycursor.execute(f"UPDATE tache SET date_de_realisation = '{completion_date}' WHERE id_tache = '{id_tache}'")
                    update_table(event)
            else:
                messagebox.showerror("Erreur", f"La tâche '{selected_task_name}' est déjà terminée.")
        else:
            messagebox.showerror("Erreur", "Tâche non trouvée dans la base de données")
    else :
        messagebox.showerror("Erreur", "Veuillez d'abord sélectionner une tâche à terminée.")
   
# endregion : FINALISER UNE TACHE


# region : SUPPRIMER UNE TACHE
def delete_task_window(event):
    selected_item = table.selection()
    if selected_item:
        selected_task_name = table.item(selected_item)["values"][1] #Le 1 correspond à la colonne tâche
        
        # Requête pour obtenir l'id_tache en fonction du nom de la tâche
        mycursor.execute(f"SELECT id_tache, id_etat FROM tache WHERE nom_tache = %s", (selected_task_name,))
        query_result = mycursor.fetchone()
        mycursor.fetchall()

        if query_result:
            id_tache = query_result.get('id_tache')
            
            confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer la tâche '{selected_task_name}'?")
               
            if confirmation:
                mycursor.execute(f"DELETE FROM tache WHERE id_tache = '{id_tache}'")
            
                update_table(event)
        else:
            messagebox.showerror("Erreur", "Tâche non trouvée dans la base de données")
    else :
        messagebox.showerror("Erreur", "Veuillez d'abord sélectionner une tâche à supprimée.")
    
# endregion : SUPPRIMER UNE TACHE


# region : PROGRAMME

# execution du programme
database()
window_app()
           
# Affichage de la fenetre
display_list.mainloop()

# endregion : PROGRAMME