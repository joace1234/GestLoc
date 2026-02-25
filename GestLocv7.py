import customtkinter as ctk
import sqlite3
from tkinter import messagebox


# Configurations Globale
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
DB_NAME = "GestLoc.db"

# =========================================================
# SYSTEME DE BASE DE DONNEES (OPTIMISÉ)
# =========================================================
def execute_query(query, params=(), fetch=False, lastrowid=False):
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(query, params)
        res = cursor.fetchall() if fetch else (cursor.lastrowid if lastrowid else None)
        conn.commit()
        conn.close()
        return res
    except sqlite3.Error as e:
        messagebox.showerror("Erreur SQL", f"Détails : {e}")
        return None

def init_db():
    # Création de toutes les tables selon la logique main.py original
    tables = [
        """CREATE TABLE IF NOT EXISTS info_immeuble(id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, nb_niv INTEGER, prix_m2 REAL, nom_proprietaire TEXT, num_proprietaire TEXT)""",
        """CREATE TABLE IF NOT EXISTS appartement(id INTEGER PRIMARY KEY AUTOINCREMENT, immeuble_id INTEGER, niveau TEXT, numero INTEGER, nb_pieces INTEGER, FOREIGN KEY(immeuble_id) REFERENCES info_immeuble(id))""",
        """CREATE TABLE IF NOT EXISTS piece(id INTEGER PRIMARY KEY AUTOINCREMENT, appartement_id INTEGER, surface REAL, FOREIGN KEY(appartement_id) REFERENCES appartement(id))""",
        """CREATE TABLE IF NOT EXISTS locataire(id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, postnom TEXT, prenom TEXT, lieu_date_naiss TEXT, taille INTEGER, date_begin TEXT, immeuble_id INTEGER, appartement_id INTEGER, FOREIGN KEY(immeuble_id) REFERENCES info_immeuble(id), FOREIGN KEY(appartement_id) REFERENCES appartement(id))""",
        """CREATE TABLE IF NOT EXISTS loyer(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, montant REAL, locataire_id INTEGER, FOREIGN KEY(locataire_id) REFERENCES locataire(id))"""
    ]
    for t in tables: execute_query(t)

# =========================================================
# GESTION DES IMMEUBLES ET APPARTEMENTS
# =========================================================
def PageImmeuble():
    app = ctk.CTk()
    app.title("GesLoc V7 - Immeubles")
    app.geometry("600x500")

    ctk.CTkLabel(app, text="NOUVEL IMMEUBLE", font=("Arial Black", 18)).pack(pady=20)
    frame = ctk.CTkFrame(app)
    frame.pack(padx=20, pady=10, fill="both")

    entries = {}
    for label in ["Adresse", "Niveaux", "Prix m2", "Propriétaire", "Contact"]:
        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=10)
        ctk.CTkLabel(row, text=label, width=120).pack(side="left")
        en = ctk.CTkEntry(row)
        en.pack(side="right", expand=True, fill="x")
        entries[label] = en

    def sauvegarder():
        try:
            imm_id = execute_query(
                "INSERT INTO info_immeuble (adresse, nb_niv, prix_m2, nom_proprietaire, num_proprietaire) VALUES (?,?,?,?,?)",
                (entries["Adresse"].get(), int(entries["Niveaux"].get()), float(entries["Prix m2"].get()), entries["Propriétaire"].get(), entries["Contact"].get()),
                lastrowid=True
            )
            messagebox.showinfo("Succès", "Immeuble enregistré !")
            app.destroy()
            Principale()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez remplir correctement les chiffres.")

    ctk.CTkButton(app, text="Enregistrer l'immeuble", command=sauvegarder).pack(pady=20)
    ctk.CTkButton(app, text="Retour", fg_color="gray", command=lambda:(app.destroy(), Principale())).pack()
    app.mainloop()

# =========================================================
# GESTION DES LOCATAIRES (V7 DYNAMIQUE)
# =========================================================
def PageLocataire():
    app = ctk.CTk()
    app.title("GesLoc V7 - Locataires")
    app.geometry("800x600")

    ctk.CTkLabel(app, text="GESTION DES LOCATAIRES", font=("Arial Black", 20)).pack(pady=20)

    btn_frame = ctk.CTkFrame(app, fg_color="transparent")
    btn_frame.pack(pady=10)

    def open_new_loc():
        app.destroy()
        NewLocForm()

    ctk.CTkButton(btn_frame, text="Nouveau Locataire", command=open_new_loc).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Paiement Loyer", command=lambda:(app.destroy(), PageLoyer())).pack(side="left", padx=10)
    
    # Tableau simplifié des locataires
    scroll = ctk.CTkScrollableFrame(app, width=750, height=350)
    scroll.pack(pady=20, padx=20)

    data = execute_query("""
        SELECT l.id, l.nom, l.prenom, i.adresse FROM locataire l 
        LEFT JOIN info_immeuble i ON l.immeuble_id = i.id
    """, fetch=True)

    if data:
        for item in data:
            row = ctk.CTkFrame(scroll)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"ID: {item[0]} | {item[1]} {item[2]} | Lieu: {item[3]}").pack(side="left", padx=10)
    else:
        ctk.CTkLabel(scroll, text="Aucun locataire enregistré").pack(pady=20)

    ctk.CTkButton(app, text="Retour Menu", fg_color="gray", command=lambda:(app.destroy(), Principale())).pack(pady=10)
    app.mainloop()

def NewLocForm():
    app = ctk.CTk()
    app.title("Inscription")
    app.geometry("600x500")

    # Récupération dynamique des immeubles pour la ComboBox
    immeubles = execute_query("SELECT id, adresse FROM info_immeuble", fetch=True)
    imm_map = {f"{i[1]} (ID:{i[0]})": i[0] for i in immeubles} if immeubles else {"Créer immeuble d'abord": 0}

    ctk.CTkLabel(app, text="NOUVEAU LOCATAIRE", font=("Arial Black", 16)).pack(pady=20)
    
    nom = ctk.CTkEntry(app, placeholder_text="Nom")
    nom.pack(pady=5)
    prenom = ctk.CTkEntry(app, placeholder_text="Prénom")
    prenom.pack(pady=5)
    combo_imm = ctk.CTkComboBox(app, values=list(imm_map.keys()))
    combo_imm.pack(pady=10)

    def save():
        execute_query("INSERT INTO locataire (nom, prenom, immeuble_id) VALUES (?,?,?)",
                      (nom.get(), prenom.get(), imm_map[combo_imm.get()]))
        messagebox.showinfo("OK", "Enregistré")
        app.destroy()
        PageLocataire()

    ctk.CTkButton(app, text="Valider", command=save).pack(pady=20)
    app.mainloop()

# =========================================================
# GESTION DES LOYERS
# =========================================================
def PageLoyer():
    app = ctk.CTk()
    app.title("Paiements")
    app.geometry("500x400")

    locataires = execute_query("SELECT id, nom, prenom FROM locataire", fetch=True)
    loc_