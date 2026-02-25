import customtkinter as ctk
import sqlite3

conn1 = sqlite3.connect("GestLoc.db")
conn1.execute("PRAGMA foreign_keys = ON")
cursor= conn1.cursor()

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS info_immeuble(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adresse TEXT, 
    nb_niv INTEGER, 
    prix_m2 REAL, 
    nom_proprietaire TEXT, 
    num_proprietaire TEXT
)               
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appartement(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    immeuble_id INTEGER NOT NULL,
    niveau TEXT NOT NULL,
    numero INTEGER NOT NULL,
    nb_pieces INTEGER NOT NULL,
    FOREIGN KEY (immeuble_id) REFERENCES info_immeuble(id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS piece(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appartement_id INTEGER NOT NULL,
    surface REAL NOT NULL,
    FOREIGN KEY (appartement_id) REFERENCES appartement(id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS locataire(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    postnom TEXT,
    prenom TEXT,
    lieu_date_naiss TEXT,
    taille INTEGER,
    date_begin TEXT,
    immeuble_id INTEGER,
    appartement_id INTEGER,
    FOREIGN KEY (immeuble_id) REFERENCES info_immeuble(id),
    FOREIGN KEY (appartement_id) REFERENCES appartement(id)
)
    
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS loyer(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    montant REAL,
    locataire_id INTEGER,
    FOREIGN KEY (locataire_id) REFERENCES locataire(id)
)
""")

conn1.close()    # Ferme la connexion
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def EnregLoyer(date, montant, locataire_id):
    conn = sqlite3.connect("GestLoc.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO loyer(date, montant, locataire_id)
        VALUES (?, ?, ?)
    """, (date, montant, locataire_id))

    conn.commit()
    conn.close()
    
def enregistrer_immeuble(adresse, nb_niv, prix_m2, nom_proprietaire, num_proprietaire):
    conn = sqlite3.connect("GestLoc.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO info_immeuble(adresse, nb_niv, prix_m2, nom_proprietaire, num_proprietaire)
        VALUES (?, ?, ?, ?, ?)
    """, (adresse, nb_niv, prix_m2, nom_proprietaire, num_proprietaire))
    immeuble_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return immeuble_id

def enregistrer_appartement(immeuble_id, niveau, numero, nb_pieces):
    conn = sqlite3.connect("GestLoc.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appartement(immeuble_id, niveau, numero, nb_pieces)
        VALUES (?, ?, ?, ?)
    """, (immeuble_id, niveau, numero, nb_pieces))
    appartement_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return appartement_id

def enregistrer_piece(appartement_id, surface):
    conn = sqlite3.connect("GestLoc.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO piece(appartement_id, surface)
        VALUES (?, ?)
    """, (appartement_id, surface))
    conn.commit()
    conn.close()
    
def enregistrer_locataire(nom, postnom, prenom, lieu_date_naiss, taille, date_begin, immeuble_id, appartement_id): 
    conn = sqlite3.connect("GestLoc.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO locataire(
            nom, postnom, prenom, lieu_date_naiss, 
            taille, date_begin, immeuble_id, appartement_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nom, postnom, prenom, lieu_date_naiss, taille, date_begin, immeuble_id, appartement_id))

    conn.commit()
    conn.close()
# ==========================
# PAGE DIMENSIONS DES PIECES
# ==========================
def DimensionsPieces(pieces_data):
    app = ctk.CTk()
    app.title("GesLoc")
    app.geometry("900x700+100+20")
    app.resizable(False, False)

    title = ctk.CTkLabel(app, text="Dimensions des pièces (m²)", font=('Arial Black', 16))
    title.pack(pady=20)

    scroll_frame = ctk.CTkScrollableFrame(app, width=850, height=490)
    scroll_frame.pack(pady=10)

    entries = {}

    for niveau, appartements in pieces_data.items():
        frame_niveau = ctk.CTkFrame(scroll_frame)
        frame_niveau.pack(pady=10, fill="x", padx=10)

        label_niv = ctk.CTkLabel(frame_niveau, text=f"Niveau {niveau}", font=('Arial Black', 14))
        label_niv.pack(anchor="w", pady=5)

        entries[niveau] = {}

        # Boucle adaptée pour les listes
        for appart_index, nb_pieces in enumerate(appartements, start=1):
            frame_app = ctk.CTkFrame(frame_niveau)
            frame_app.pack(pady=5, fill="x", padx=20)

            label_app = ctk.CTkLabel(frame_app, text=f"Appartement {appart_index}", font=('Arial Narrow', 13))
            label_app.pack(anchor="w")

            entries[niveau][appart_index] = []

            for piece in range(1, nb_pieces + 1):
                frame_piece = ctk.CTkFrame(frame_app)
                frame_piece.pack(pady=3, fill="x", padx=30)

                label_piece = ctk.CTkLabel(frame_piece, text=f"Pièce {piece} (m²) :")
                label_piece.pack(side="left", padx=10)

                entry_dim = ctk.CTkEntry(frame_piece, placeholder_text="Ex: 40")
                entry_dim.pack(side="left", padx=10)

                entries[niveau][appart_index].append(entry_dim)

    # Nouvelle fonction pour enregistrer toutes les données
    def enregistrer_dimensions():
        conn = sqlite3.connect("GestLoc.db")
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        # Parcours de tous les niveaux et appartements
        for niveau, appartements in entries.items():
            for appart_index, piece_entries in appartements.items():
                # On crée ou récupère l'appartement dans la base
                cursor.execute("""
                    INSERT INTO appartement(immeuble_id, niveau, numero, nb_pieces)
                    VALUES (?, ?, ?, ?)
                """, (immeuble_id_global, str(niveau), appart_index, len(piece_entries)))
                appartement_id = cursor.lastrowid

                # On enregistre chaque pièce
                for entry_dim in piece_entries:
                    try:
                        surface = float(entry_dim.get())
                        cursor.execute("""
                            INSERT INTO piece(appartement_id, surface)
                            VALUES (?, ?)
                        """, (appartement_id, surface))
                    except ValueError:
                        print(f"Valeur non valide pour une pièce dans appart {appart_index}, niveau {niveau}")

        conn.commit()
        conn.close()
        print("Toutes les données des appartements et pièces ont été enregistrées !")
        app.destroy()
        Principale()

    button_enregistrer = ctk.CTkButton(app, text="Enregistrer", command=enregistrer_dimensions)
    button_enregistrer.pack(pady=10)

    button_retour = ctk.CTkButton(app, text="Retour au menu", command=lambda: (app.destroy(), Principale()))
    button_retour.pack(pady=10)

    app.mainloop()


# ==========================
# PAGE NOMBRE DE PIECES
# ==========================
def NbPiecesParAppartement(apparts_par_niveau):
    app = ctk.CTk()
    app.title("GesLoc")
    app.geometry("800x650+200+20")
    app.resizable(False, False)

    title = ctk.CTkLabel(app, text="Nombre de pièces par appartement", font=('Arial Black', 16))
    title.pack(pady=20)

    scroll_frame = ctk.CTkScrollableFrame(app, width=750, height=450)
    scroll_frame.pack()

    entries = {}
#------
    for index, nb_apparts in enumerate(apparts_par_niveau):

        # Gestion du nom du niveau
        if index == 0:
            nom_niveau = "Rez-de-chaussée"
            niveau_key = "Rez-de-chaussée"
        else:
            nom_niveau = f"Niveau {index}"
            niveau_key = index

        frame_niveau = ctk.CTkFrame(scroll_frame)
        frame_niveau.pack(pady=10, fill="x")

        label_niv = ctk.CTkLabel(frame_niveau,text=nom_niveau,font=('Arial Black', 14))
        label_niv.pack(anchor="w")

        entries[niveau_key] = []

        for appart in range(1, nb_apparts + 1):

            frame_app = ctk.CTkFrame(frame_niveau)
            frame_app.pack(pady=5, padx=20)

            label_app = ctk.CTkLabel(frame_app, text=f"Appartement {appart} :")
            label_app.pack(side="left", padx=10)

            entry_piece = ctk.CTkEntry(frame_app, placeholder_text="Nombre de pièces")
            entry_piece.pack(side="left", padx=10)

            entries[niveau_key].append(entry_piece)
#-----
    
    def go_to_dimensions():
        pieces_data = {}
        for niv, entry_list in entries.items():
            pieces_data[niv] = []
            for e in entry_list:
                pieces_data[niv].append(int(e.get()))
        app.destroy()
        DimensionsPieces(pieces_data)

    ctk.CTkButton(app, text="Suivant", command=go_to_dimensions).pack()
    app.mainloop()

# ==========================
# PAGE INFO APPARTEMENTS PAR NIVEAU
# ==========================
def InfoAppart(nb_niv):
    global immeuble_id_global  # ID de l'immeuble enregistré précédemment
    app = ctk.CTk()
    app.title("GesLoc")
    app.geometry("800x600+400+50")
    app.resizable(False, False)

    label = ctk.CTkLabel(app, text="Nombre d'appartements par niveau", font=('Arial Black', 16))
    label.pack(pady=20)
    frame = ctk.CTkFrame(app)
    frame.pack(pady=10)

    label_rez = ctk.CTkLabel(frame, text="Rez de chaussé", font=('Arial Narrow', 14))
    label_rez.pack(side="left", padx=10)

    entry_rez = ctk.CTkEntry(frame, placeholder_text="Nombre d'appartements niveau au rez de chaussé")
    entry_rez.pack(side="left", padx=10)
    entries = []

    # Création dynamique des niveaux

    for i in range(nb_niv):
        frame = ctk.CTkFrame(app)
        frame.pack(pady=10)

        label_niv = ctk.CTkLabel(frame, text=f"Niveau {i+1} :", font=('Arial Narrow', 14))
        label_niv.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, placeholder_text=f"Nombre d'appartements niveau {i+1}")
        entry.pack(side="left", padx=10)

        entries.append(entry)

    # Bouton Suivant vers page pièces
    def go_to_pieces():
        try:
            apparts_par_niveau = [int(entry_rez.get())] + [int(e.get()) for e in entries]

            #  Enregistrement des appartements
            pieces_data = {}  # dictionnaire pour DimensionsPieces
            for niveau_index, nb_apparts in enumerate(apparts_par_niveau):
                if niveau_index == 0:
                    niveau_name = "Rez-de-chaussée"
                else:
                    niveau_name = f"Niveau {niveau_index}"
                pieces_data[niveau_name] = []     
                pieces_data[niveau_name].append(0)  # on mettra les surfaces plus tard dans DimensionsPieces

            app.destroy()
            NbPiecesParAppartement(apparts_par_niveau)

        except ValueError:
            print("Entrez des nombres valides")

    ctk.CTkButton(app, text="Suivant", command=go_to_pieces).pack(pady=20)
    app.mainloop()
# ==========================
# PAGE APPARTEMENT
# ==========================
def Appartement():
    app = ctk.CTk()
    app.title("GesLoc")
    app.geometry("800x600+400+50")
    app.resizable(False, False)

    label = ctk.CTkLabel(app,text="Information sur l'immeuble", font=('Arial Black', 16)).place(x=280, y=10)
    # Adresse
    ctk.CTkLabel(app,text="Adresse de l'immeuble :",font=('Arial Narrow', 14)).place(x=10, y=50)
    
    zone1 = ctk.CTkEntry(app,placeholder_text="Adresse de l'immeuble")
    zone1.place(x=200, y=50)




    # Nombre de niveaux
    ctk.CTkLabel(app, text="Nombre de niveau :", font=('Arial Narrow', 14)).place(x=10, y=100)

    zone2 = ctk.CTkEntry(app, placeholder_text="Nombre de niveau")
    zone2.place(x=200, y=100)

    # Prix m2
    ctk.CTkLabel(app,text="Prix du m2 ($):", font=('Arial Narrow', 14)).place(x=10, y=150)

    zone3 = ctk.CTkEntry(app,  placeholder_text="Prix du m2")
    zone3.place(x=200, y=150)

    # Nom propriétaire
    ctk.CTkLabel(app, text="Nom complet du propriétaire :", font=('Arial Narrow', 14)).place(x=10, y=200)

    zone4 = ctk.CTkEntry(app, placeholder_text="Nom complet du propriétaire")
    zone4.place(x=200, y=200)

    # Téléphone propriétaire
    ctk.CTkLabel(app,text="N° Téléphone du propriétaire :",font=('Arial Narrow', 14)).place(x=10, y=250)

    zone5 = ctk.CTkEntry(app, placeholder_text="Téléphone du propriétaire")
    zone5.place(x=200, y=250)
    # Fonction bouton Suivant
    def go_to_info():
        global immeuble_id_global
        try:
            adresse = zone1.get()
            nb_niv = int(zone2.get())
            prix_m2 = float(zone3.get())
            nom_proprietaire = zone4.get()
            num_proprietaire = zone5.get()
            if nb_niv <= 0: raise ValueError
            immeuble_id_global = enregistrer_immeuble(adresse, nb_niv, prix_m2, nom_proprietaire, num_proprietaire)
            app.destroy()
            InfoAppart(nb_niv)
        except ValueError:
            print("Veuillez entrer des valeurs valides.")

    ctk.CTkButton(app, text='Suivant', command=go_to_info).place(x=350, y=320)
    app.mainloop()
    
# =================================
# Nouveau Locataire
#==================================

def NewLoc(): 
    app = ctk.CTk()
    app.title("GesLoc")
    app.geometry("800x600+400+50")
    app.resizable(False, False)

    label = ctk.CTkLabel(app, text="Enregistrement des nouveaux locataires", font=('Arial Black', 16))
    label.pack(pady=30)

    # ======================
    # CHAMPS
    # ======================

    ctk.CTkLabel(app, text="Nom :", font=('Arial Narrow', 14)).place(x=10, y=80)
    nom = ctk.CTkEntry(app, placeholder_text="Ex : MUTOMBO")
    nom.place(x=150, y=80)

    ctk.CTkLabel(app, text="Post-nom :", font=('Arial Narrow', 14)).place(x=10, y=120)
    postnom = ctk.CTkEntry(app, placeholder_text="Ex : MUKENDI")
    postnom.place(x=150, y=120)

    ctk.CTkLabel(app, text="Prénom :", font=('Arial Narrow', 14)).place(x=10, y=160)
    prenom = ctk.CTkEntry(app, placeholder_text="Ex : Christian")
    prenom.place(x=150, y=160)

    ctk.CTkLabel(app, text="Lieu & date de naissance :", font=('Arial Narrow', 14)).place(x=10, y=200)
    lieu_naiss_en = ctk.CTkEntry(app, placeholder_text="Ex : Kinshasa, 30/12/1998", width=250)
    lieu_naiss_en.place(x=200, y=200)

    ctk.CTkLabel(app, text="Taille de la famille :", font=('Arial Narrow', 14)).place(x=10, y=240)
    taille_en = ctk.CTkEntry(app, placeholder_text="Ex : 3")
    taille_en.place(x=200, y=240)

    ctk.CTkLabel(app, text="Date d'entrée :", font=('Arial Narrow', 14)).place(x=10, y=280)
    date_en = ctk.CTkEntry(app, placeholder_text="Ex : 12/02/2026")
    date_en.place(x=200, y=280)

    ctk.CTkLabel(app, text="Immeuble n° :", font=('Arial Narrow', 14)).place(x=10, y=320)
    # Récupération des immeubles depuis la base
    conn = sqlite3.connect("GestLoc.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, adresse FROM info_immeuble")
    immeubles = cursor.fetchall()
    conn.close()

    num_imm_en = ctk.CTkComboBox(app, values=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    num_imm_en.place(x=200, y=320)

    ctk.CTkLabel(app, text="Appartement n° :", font=('Arial Narrow', 14)).place(x=10, y=360)
    num_appart_en = ctk.CTkComboBox(app, values=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    num_appart_en.place(x=200, y=360)

    # ======================
    # FONCTION VALIDATION
    # ======================

    def valider_locataire():
        try:
            name = nom.get()
            postname = postnom.get()
            prename = prenom.get()
            ldn = lieu_naiss_en.get()
            size = int(taille_en.get())
            date_beg = date_en.get()
            number_imm = int(num_imm_en.get())
            number_appart = int(num_appart_en.get())

            if not name or not prename:
                raise ValueError

            enregistrer_locataire(
                name,
                postname,
                prename,
                ldn,
                size,
                date_beg,
                number_imm,
                number_appart
            )

            print("Locataire enregistré avec succès !")
            app.destroy()
            Principale()

        except ValueError:
            print("Veuillez remplir correctement tous les champs.")

    # ======================
    # BOUTONS
    # ======================

    button_enr = ctk.CTkButton(app, text="Enregistrer", command=valider_locataire)
    button_enr.place(x=300, y=450)

    button_retour = ctk.CTkButton(app, text="Retour", command=lambda: (app.destroy(), Principale()))
    button_retour.place(x=300, y=500)

    app.mainloop()
    
def AfficherLoyers():
    app = ctk.CTk()
    app.title("GesLoc - Paiements reçus")
    app.geometry("1100x600+100+50")
    app.resizable(False, False)

    title = ctk.CTkLabel(app, text="Liste des paiements reçus", font=('Arial Black', 18))
    title.pack(pady=20)

    scroll_frame = ctk.CTkScrollableFrame(app, width=1000, height=400)
    scroll_frame.pack(pady=10, padx=10)

    # Colonnes
    col_widths = [50, 150, 150, 150, 120]
    headers = ["ID", "Date", "Nom", "Postnom", "Montant ($)"]

    # Connexion base
    conn = sqlite3.connect("GestLoc.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # 🔥 Jointure loyer + locataire
    cursor.execute("""
        SELECT 
            l.id,
            l.date,
            loc.nom,
            loc.postnom,
            l.montant
        FROM loyer l
        JOIN locataire loc ON l.locataire_id = loc.id
        ORDER BY l.id DESC
    """)

    loyers = cursor.fetchall()
    conn.close()

    # En-têtes
    header_frame = ctk.CTkFrame(scroll_frame)
    header_frame.pack(fill="x", pady=2)

    for i, h in enumerate(headers):
        label = ctk.CTkLabel(header_frame, text=h, width=col_widths[i], anchor="w", font=('Arial Bold', 12))
        label.pack(side="left", padx=2)

    # Données
    if loyers:
        for row in loyers:
            row_frame = ctk.CTkFrame(scroll_frame)
            row_frame.pack(fill="x", pady=1)

            for i, value in enumerate(row):
                label = ctk.CTkLabel(row_frame, text=str(value), width=col_widths[i], anchor="w")
                label.pack(side="left", padx=2)
    else:
        ctk.CTkLabel(scroll_frame, text="Aucun paiement enregistré", font=('Arial', 14)).pack(pady=20)

    # Bouton retour
    ctk.CTkButton(app, text="Retour", command=lambda: (app.destroy(), Locataire())).pack(pady=15)

    app.mainloop()    
def loyer(): 
    app = ctk.CTk()
    app.title("GesLoc - Liste des Locataires")
    app.geometry("1200x700+100+50")
    app.resizable(False, False)

    title = ctk.CTkLabel(app, text="Payement de loyer", font=('Arial Black', 18))
    title.pack(pady=20)
    
    ctk.CTkLabel(app, text="Date de paiement:", font=('Arial Narrow', 14)).place(x=10, y=50)
    date = ctk.CTkEntry(app, placeholder_text="Ex : Le 12/02/2026")
    date.place(x=150, y=50)
    ctk.CTkLabel(app, text="Montant:", font=('Arial Narrow', 14)).place(x=10, y=100)
    montant = ctk.CTkEntry(app, placeholder_text="Ex : 500")
    montant.place(x=150, y=100)
    
    ctk.CTkLabel(app, text="Nom du locateur (Payé):", font=('Arial Narrow', 14)).place(x=10, y=150)
    conn = sqlite3.connect("GestLoc.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, postnom, prenom FROM locataire")
    locataires = cursor.fetchall()
    conn.close()

    locataire_dict = {
        f"{l[1]} {l[2]} {l[3]}": l[0]
        for l in locataires
    }

    combo_locataire = ctk.CTkComboBox(
        app,
        values=list(locataire_dict.keys())
    )
    combo_locataire.place(x=150, y=150)
    
    def valider_loyer():
        try:
            date1 = date.get()
            montant1 = float(montant.get())
            nom_selectionne = combo_locataire.get()

            if not date1 or not nom_selectionne:
                raise ValueError

            # 🔥 récupérer le vrai ID
            locataire_id = locataire_dict[nom_selectionne]

            EnregLoyer(date1, montant1, locataire_id)

            print("Loyer enregistré avec succès !")

        except Exception as e:
            print("Erreur :", e)
    
    button = ctk.CTkButton(app, text='Enregistrer', command=valider_loyer)
    button.place(x=150, y=200)
    
    button = ctk.CTkButton(app, text='Retour', command=lambda: (app.destroy(), Locataire()))
    button.place(x=150, y=250)
    
    app.mainloop()
    
# ==========================
# PAGE AFFICHER LOCATAIRES
# ==========================
def AfficherLocataires():
    app = ctk.CTk()
    app.title("GesLoc - Liste des Locataires")
    app.geometry("1200x700+100+50")
    app.resizable(False, False)

    title = ctk.CTkLabel(app, text="Liste des Locataires", font=('Arial Black', 18))
    title.pack(pady=20)

    scroll_frame = ctk.CTkScrollableFrame(app, width=1050, height=500)
    scroll_frame.pack(pady=10, padx=10)

    # Colonnes: ID, Nom, Postnom, Prénom, Lieu/Date Naiss, Taille Famille, Date Entrée, Immeuble, Appartement
    col_widths = [30, 150, 150, 150, 220, 120, 120, 200, 120]
    headers = ["ID", "Nom", "Postnom", "Prénom", "Lieu & Date Naissance", "Taille Famille", "Date Entrée", "Immeuble", "Appartement"]

    # Connexion à la base pour récupérer les données
    conn = sqlite3.connect("GestLoc.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Requête avec jointures pour obtenir les infos complètes
    cursor.execute("""
        SELECT 
            l.id,
            l.nom,
            l.postnom,
            l.prenom,
            l.lieu_date_naiss,
            l.taille,
            l.date_begin,
            i.adresse,
            a.numero
        FROM locataire l
        LEFT JOIN info_immeuble i ON l.immeuble_id = i.id
        LEFT JOIN appartement a ON l.appartement_id = a.id
        ORDER BY l.id
    """)
    locataires = cursor.fetchall()
    conn.close()

    # En-têtes du tableau
    header_frame = ctk.CTkFrame(scroll_frame)
    header_frame.pack(fill="x", padx=2, pady=2)
    for i, h in enumerate(headers):
        label = ctk.CTkLabel(header_frame, text=h, width=col_widths[i], anchor="w", font=('Arial Bold', 11))
        label.pack(side="left", padx=2)

    # Lignes de données
    if locataires:
        for loc in locataires:
            ligne_frame = ctk.CTkFrame(scroll_frame)
            ligne_frame.pack(fill="x", padx=2, pady=1)

            for i, valeur in enumerate(loc):
                # Formater la valeur
                text = str(valeur) if valeur is not None else "-"
                label = ctk.CTkLabel(ligne_frame, text=text, width=col_widths[i], anchor="w")
                label.pack(side="left", padx=2)
    else:
        # Message si aucun locataire
        label_vide = ctk.CTkLabel(scroll_frame, text="Aucun locataire enregistré", font=('Arial', 14))
        label_vide.pack(pady=20)

    # Boutons
    btn_frame = ctk.CTkFrame(app)
    btn_frame.pack(pady=15)

    btn_retour = ctk.CTkButton(btn_frame, text="Retour", command=lambda: (app.destroy(), Locataire()))
    btn_retour.pack(side="left", padx=10)

    app.mainloop()

# ==========================
# PAGE LOCATAIRE
# ==========================
def Locataire():
    app = ctk.CTk()
    app.title("GesLoc")
    app.geometry("800x600+400+50")
    app.resizable(False, False)

    label = ctk.CTkLabel(app,text="Gestion des Locataires", font=('Arial Black', 16))
    label.pack(pady=50)

    button_new_loc = ctk.CTkButton(app, text="Enregistrement des nouveaux locataire", command=lambda: (app.destroy(), NewLoc()))
    button_new_loc.pack(pady=20)
    
    button_afficher_loc = ctk.CTkButton(app, text="Afficher les locataires", command=lambda: (app.destroy(), AfficherLocataires()))
    button_afficher_loc.pack(pady=20)
    
    button_retour = ctk.CTkButton(app, text="Paiment des loyer", command=lambda: (app.destroy(), loyer()))
    button_retour.pack(pady=20)
    button_loyers = ctk.CTkButton(
    app,
    text="Afficher les paiements reçus",
    command=lambda: (app.destroy(), AfficherLoyers())
)
    button_loyers.pack(pady=20)
    menu_principale = ctk.CTkButton(app, text="Retour au menu principale", command=lambda: (app.destroy(), Principale()))
    menu_principale.pack(pady=20)
    
 
    app.mainloop()
    
    
    

# ==========================
# PAGE PRINCIPALE
# ==========================
def Principale():
    app = ctk.CTk()
    app.title("GesLoc")
    app.geometry("800x600+400+50")
    app.resizable(False, False)

    label = ctk.CTkLabel(app, text='GEST LOC APP', font=('Arial Black', 20, 'bold'))
    label.place(x=300, y=50)

    # Fonction dynamique pour la gestion des appartements
    def gestion_appartements():
        app.destroy()  # Fermer la page principale
        # Connexion à la base
        conn = sqlite3.connect("GestLoc.db")
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM info_immeuble")
        immeubles = cursor.fetchall()
        conn.close()

        if not immeubles:
            # Aucun immeuble -> ouvrir formulaire comme avant
            Appartement()
        else:
            # Immeubles existants -> afficher tableau
            def AfficherImmeubles():
                tableau_app = ctk.CTk()
                tableau_app.title("Immeubles enregistrés")
                tableau_app.geometry("1050x700+200+50")
                tableau_app.resizable(False, False)

                title = ctk.CTkLabel(tableau_app, text="Immeubles enregistrés", font=('Arial Black', 16))
                title.pack(pady=15)

                scroll_frame = ctk.CTkScrollableFrame(tableau_app, width=1000, height=450)
                scroll_frame.pack(pady=5, padx=5)

                # Colonnes principales : ID, Adresse, Niveaux, Prix/m², Propriétaire, Téléphone, Nb Appartements
                col_widths = [40, 250, 60, 70, 200, 150, 70]
                headers = ["ID", "Adresse", "Niveaux", "Prix/m²", "Propriétaire", "Téléphone", "Nb Apparts"]

                # Connexion à la base
                conn = sqlite3.connect("GestLoc.db")
                conn.execute("PRAGMA foreign_keys = ON")
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM info_immeuble")
                immeubles = cursor.fetchall()

                # Calcul du nombre d'appartements par immeuble
                nb_apparts_dict = {}
                prix_appart_dict = {}  # pour stocker le prix par appartement
                for immeuble in immeubles:
                    immeuble_id = immeuble[0]
                    prix_m2 = immeuble[3]  # colonne prix_m2

                    # Nombre d'appartements
                    cursor.execute("SELECT id FROM appartement WHERE immeuble_id = ?", (immeuble_id,))
                    apparts = cursor.fetchall()
                    nb_apparts_dict[immeuble_id] = len(apparts)

                    # Prix par appartement
                    prix_appart_dict[immeuble_id] = {}
                    for a in apparts:
                        appart_id = a[0]
                        # Somme des surfaces des pièces
                        cursor.execute("SELECT SUM(surface) FROM piece WHERE appartement_id = ?", (appart_id,))
                        total_surface = cursor.fetchone()[0] or 0
                        prix_appart_dict[immeuble_id][appart_id] = total_surface * prix_m2

                conn.close()

                # En-têtes du tableau
                header_frame = ctk.CTkFrame(scroll_frame)
                header_frame.pack(fill="x", padx=2, pady=2)
                for i, h in enumerate(headers):
                    label = ctk.CTkLabel(header_frame, text=h, width=col_widths[i], anchor="w", font=('Arial Bold', 12))
                    label.pack(side="left", padx=2)

                # Lignes principales + sous-lignes pour appartements
                for immeuble in immeubles:
                    ligne_frame = ctk.CTkFrame(scroll_frame)
                    ligne_frame.pack(fill="x", padx=2, pady=1)

                    id_immeuble = immeuble[0]
                    valeurs = list(immeuble) + [nb_apparts_dict.get(id_immeuble, 0)]  # ajouter nb_apparts à la fin

                    for i, valeur in enumerate(valeurs):
                        label = ctk.CTkLabel(ligne_frame, text=str(valeur), width=col_widths[i], anchor="w")
                        label.pack(side="left", padx=2)

                    # Sous-lignes : prix par appartement
                    for appart_id, prix in prix_appart_dict.get(id_immeuble, {}).items():
                        sous_frame = ctk.CTkFrame(scroll_frame)
                        sous_frame.pack(fill="x", padx=50, pady=1)

                        label_sous = ctk.CTkLabel(
                            sous_frame,
                            text=f"Appartement {appart_id} : {prix:.2f} $",
                            anchor="w"
                        )
                        label_sous.pack(side="left")

                    # Calcul du total de l'immeuble
                    total_immeuble = sum(prix_appart_dict.get(id_immeuble, {}).values())

                    # Ligne total
                    total_frame = ctk.CTkFrame(scroll_frame)
                    total_frame.pack(fill="x", padx=50, pady=5)

                    label_tot = ctk.CTkLabel(
                        total_frame,
                        text=f"Total des revenus de l'immeuble : {total_immeuble:.2f} $",
                        font=('Arial Black', 12),
                        anchor="w"
                    )
                    label_tot.pack(side="left")

                # Bouton pour ajouter un nouvel immeuble
                btn_ajouter = ctk.CTkButton(
                    tableau_app,
                    text="Ajouter un nouvel immeuble",
                    command=lambda: (tableau_app.destroy(), Appartement())
                )
                btn_ajouter.pack(pady=10)

                # Bouton retour
                btn_retour = ctk.CTkButton(tableau_app, text="Retour au menu", command=lambda: (tableau_app.destroy(), Principale()))
                btn_retour.pack(pady=5)

                tableau_app.mainloop()

            AfficherImmeubles()

    # Bouton Gestion des appartements
    button = ctk.CTkButton(app, text='Gestion des appartements', width=200, height=45, command=gestion_appartements)
    button.place(x=300, y=150)

    # Bouton Gestion des locataires
    button2 = ctk.CTkButton(app, text='Gestion des locataires', width=200, height=45, command=lambda: (app.destroy(), Locataire()))
    button2.place(x=300, y=250)

    app.mainloop()

# ==========================
# LANCEMENT APPLICATION
# ==========================
Principale()