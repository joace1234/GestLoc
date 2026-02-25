import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Configuration globale
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

DB_NAME = "GestLoc.db"

# =========================================================
# LOGIQUE BASE DE DONNÉES
# =========================================================
def execute_query(query, params=(), fetch=False, lastrowid=False):
    """Fonction utilitaire pour centraliser les appels SQL"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        result = None
        if fetch:
            result = cursor.fetchall()
        if lastrowid:
            result = cursor.lastrowid
            
        conn.commit()
        conn.close()
        return result
    except sqlite3.Error as e:
        messagebox.showerror("Erreur Base de données", f"Erreur : {e}")
        return None

def initialiser_db():
    queries = [
        """CREATE TABLE IF NOT EXISTS info_immeuble(
            id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, nb_niv INTEGER, 
            prix_m2 REAL, nom_proprietaire TEXT, num_proprietaire TEXT)""",
        """CREATE TABLE IF NOT EXISTS appartement(
            id INTEGER PRIMARY KEY AUTOINCREMENT, immeuble_id INTEGER, niveau TEXT, 
            numero INTEGER, nb_pieces INTEGER, FOREIGN KEY(immeuble_id) REFERENCES info_immeuble(id))""",
        """CREATE TABLE IF NOT EXISTS piece(
            id INTEGER PRIMARY KEY AUTOINCREMENT, appartement_id INTEGER, surface REAL, 
            FOREIGN KEY(appartement_id) REFERENCES appartement(id))""",
        """CREATE TABLE IF NOT EXISTS locataire(
            id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, postnom TEXT, prenom TEXT, 
            lieu_date_naiss TEXT, taille INTEGER, date_begin TEXT, 
            immeuble_id INTEGER, appartement_id INTEGER, 
            FOREIGN KEY(immeuble_id) REFERENCES info_immeuble(id),
            FOREIGN KEY(appartement_id) REFERENCES appartement(id))""",
        """CREATE TABLE IF NOT EXISTS loyer(
            id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, montant REAL, 
            locataire_id INTEGER, FOREIGN KEY(locataire_id) REFERENCES locataire(id))"""
    ]
    for q in queries:
        execute_query(q)

# =========================================================
# INTERFACE : NOUVEAU LOCATAIRE (V6 DYNAMIQUE)
# =========================================================
def NewLoc():
    app = ctk.CTk()
    app.title("GesLoc - Inscription Locataire")
    app.geometry("800x700+400+50")

    ctk.CTkLabel(app, text="ENREGISTREMENT LOCATAIRE", font=('Arial Black', 20)).pack(pady=20)

    form_frame = ctk.CTkFrame(app)
    form_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Dictionnaire pour stocker les entrées
    entries = {}
    fields = [("Nom", "NOM"), ("Postnom", "POSTNOM"), ("Prenom", "PRENOM"), 
              ("Lieu/Date Naiss", "Kinshasa, 01/01/2000"), ("Taille Famille", "Ex: 4"), ("Date Entrée", "DD/MM/YYYY")]

    for label, placeholder in fields:
        row = ctk.CTkFrame(form_frame, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=20)
        ctk.CTkLabel(row, text=label, width=150, anchor="w").pack(side="left")
        en = ctk.CTkEntry(row, placeholder_text=placeholder, width=250)
        en.pack(side="right")
        entries[label] = en

    # --- Sélection dynamique Immeuble ---
    row_imm = ctk.CTkFrame(form_frame, fg_color="transparent")
    row_imm.pack(fill="x", pady=5, padx=20)
    ctk.CTkLabel(row_imm, text="Immeuble", width=150, anchor="w").pack(side="left")
    
    immeubles_data = execute_query("SELECT id, adresse FROM info_immeuble", fetch=True)
    imm_options = {f"{i[1]} (ID:{i[0]})": i[0] for i in immeubles_data} if immeubles_data else {"Aucun immeuble": 0}
    
    combo_imm = ctk.CTkComboBox(row_imm, values=list(imm_options.keys()), width=250)
    combo_imm.pack(side="right")

    def valider():
        try:
            imm_id = imm_options[combo_imm.get()]
            execute_query("""INSERT INTO locataire (nom, postnom, prenom, lieu_date_naiss, taille, date_begin, immeuble_id) 
                          VALUES (?,?,?,?,?,?,?)""", 
                          (entries["Nom"].get(), entries["Postnom"].get(), entries["Prenom"].get(), 
                           entries["Lieu/Date Naiss"].get(), int(entries["Taille Famille"].get()), 
                           entries["Date Entrée"].get(), imm_id))
            messagebox.showinfo("Succès", "Locataire enregistré !")
            app.destroy()
            Locataire()
        except:
            messagebox.showerror("Erreur", "Vérifiez les champs (Taille famille doit être un nombre)")

    ctk.CTkButton(app, text="Enregistrer", command=valider).pack(pady=10)
    ctk.CTkButton(app, text="Retour", fg_color="gray", command=lambda:(app.destroy(), Locataire())).pack(pady=5)
    app.mainloop()

# =========================================================
# MENU PRINCIPAL & AUTRES
# =========================================================
def Locataire():
    app = ctk.CTk()
    app.title("Gestion Locataires")
    app.geometry("500x500")
    
    ctk.CTkLabel(app, text="MENU LOCATAIRES", font=("Arial Black", 18)).pack(pady=30)
    ctk.CTkButton(app, text="Ajouter Locataire", command=lambda:(app.destroy(), NewLoc())).pack(pady=10)
    ctk.CTkButton(app, text="Retour Menu", command=lambda:(app.destroy(), Principale())).pack(pady=10)
    app.mainloop()

def Principale():
    app = ctk.CTk()
    app.title("GestLoc V6")
    app.geometry("600x400")
    
    ctk.CTkLabel(app, text="GEST LOC - VERSION 6", font=("Arial Black", 22)).pack(pady=40)
    
    btn_frame = ctk.CTkFrame(app, fg_color="transparent")
    btn_frame.pack(pady=20)
    
    ctk.CTkButton(btn_frame, text="GESTION IMMEUBLES", width=200, height=50).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="GESTION LOCATAIRES", width=200, height=50, 
                  command=lambda:(app.destroy(), Locataire())).pack(side="left", padx=10)
    
    app.mainloop()

if __name__ == "__main__":
    initialiser_db()
    Principale()