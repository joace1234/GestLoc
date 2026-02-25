import customtkinter as ctk
import sqlite3
from tkinter import messagebox, ttk

# Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GestLocApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GestLoc V8 - Système de Gestion Intégré")
        self.geometry("1100x700")
        
        # Initialisation Base de données
        self.init_db()
        
        # Conteneur principal (Sidebar + Contenu)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        
        # Variable pour stocker la frame actuelle
        self.current_frame = None
        self.show_dashboard()

    # ==========================================
    # LOGIQUE BASE DE DONNEES
    # ==========================================
    def init_db(self):
        conn = sqlite3.connect("GestLoc.db")
        cursor = conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS info_immeuble(id INTEGER PRIMARY KEY AUTOINCREMENT, adresse TEXT, nb_niv INTEGER, prix_m2 REAL, nom_proprietaire TEXT, num_proprietaire TEXT);
            CREATE TABLE IF NOT EXISTS appartement(id INTEGER PRIMARY KEY AUTOINCREMENT, immeuble_id INTEGER, niveau TEXT, numero INTEGER, nb_pieces INTEGER, FOREIGN KEY(immeuble_id) REFERENCES info_immeuble(id));
            CREATE TABLE IF NOT EXISTS locataire(id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, immeuble_id INTEGER, date_entree TEXT, FOREIGN KEY(immeuble_id) REFERENCES info_immeuble(id));
            CREATE TABLE IF NOT EXISTS loyer(id INTEGER PRIMARY KEY AUTOINCREMENT, locataire_id INTEGER, montant REAL, date_paiement TEXT, FOREIGN KEY(locataire_id) REFERENCES locataire(id));
        """)
        conn.commit()
        conn.close()

    def query(self, sql, params=(), fetch=False):
        conn = sqlite3.connect("GestLoc.db")
        cursor = conn.cursor()
        cursor.execute(sql, params)
        res = cursor.fetchall() if fetch else None
        conn.commit()
        conn.close()
        return res

    # ==========================================
    # UI : BARRE LATÉRALE (NAVIGATION)
    # ==========================================
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="GestLoc V8", font=("Arial Black", 20)).pack(pady=30)
        
        btns = [
            ("🏠 Tableau de bord", self.show_dashboard),
            ("🏢 Immeubles", self.show_immeubles),
            ("👥 Locataires", self.show_locataires),
            ("💰 Loyers & Finance", self.show_finances)
        ]
        
        for text, cmd in btns:
            ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", anchor="w", command=cmd).pack(fill="x", padx=10, pady=5)

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    # ==========================================
    # VUES (PAGES)
    # ==========================================
    def show_dashboard(self):
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(self.current_frame, text="TABLEAU DE BORD", font=("Arial Black", 24)).pack(anchor="w")

        # Cartes statistiques
        stats_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)

        data_stats = [
            ("Immeubles", "SELECT COUNT(*) FROM info_immeuble"),
            ("Locataires", "SELECT COUNT(*) FROM locataire"),
            ("Total Collecté ($)", "SELECT SUM(montant) FROM loyer")
        ]

        for i, (title, sql) in enumerate(data_stats):
            val = self.query(sql, fetch=True)[0][0] or 0
            card = ctk.CTkFrame(stats_frame, width=250, height=120, corner_radius=15)
            card.grid(row=0, column=i, padx=10)
            card.grid_propagate(False)
            ctk.CTkLabel(card, text=title, font=("Arial", 14)).pack(pady=10)
            ctk.CTkLabel(card, text=str(val), font=("Arial Black", 22), text_color="#1f538d").pack()

    def show_locataires(self):
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        header = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text="LISTE DES LOCATAIRES", font=("Arial Black", 20)).pack(side="left")
        ctk.CTkButton(header, text="+ Ajouter", width=100, command=self.add_locataire_pop).pack(side="right")

        # Tableau (Treeview)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        
        tree = ttk.Treeview(self.current_frame, columns=("ID", "Nom", "Prénom", "Immeuble"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nom", text="Nom")
        tree.heading("Prénom", text="Prénom")
        tree.heading("Immeuble", text="Immeuble")
        tree.pack(fill="both", expand=True, pady=20)

        locs = self.query("SELECT l.id, l.nom, l.prenom, i.adresse FROM locataire l JOIN info_immeuble i ON l.immeuble_id = i.id", fetch=True)
        for row in locs:
            tree.insert("", "end", values=row)

    def add_locataire_pop(self):
        # Fenêtre flottante pour l'ajout
        pop = ctk.CTkToplevel(self)
        pop.title("Nouveau Locataire")
        pop.geometry("400x400")
        pop.attributes('-topmost', True)

        nom = ctk.CTkEntry(pop, placeholder_text="Nom")
        nom.pack(pady=10)
        prenom = ctk.CTkEntry(pop, placeholder_text="Prénom")
        prenom.pack(pady=10)
        
        imm_data = self.query("SELECT id, adresse FROM info_immeuble", fetch=True)
        imm_map = {i[1]: i[0] for i in imm_data}
        
        combo = ctk.CTkComboBox(pop, values=list(imm_map.keys()))
        combo.pack(pady=10)

        def save():
            self.query("INSERT INTO locataire (nom, prenom, immeuble_id) VALUES (?,?,?)", 
                       (nom.get(), prenom.get(), imm_map[combo.get()]))
            messagebox.showinfo("Succès", "Locataire ajouté")
            pop.destroy()
            self.show_locataires()

        ctk.CTkButton(pop, text="Enregistrer", command=save).pack(pady=20)

    def show_immeubles(self):
        # À compléter suivant la même logique que locataires
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        ctk.CTkLabel(self.current_frame, text="GESTION DES IMMEUBLES (V8)", font=("Arial Black", 20)).pack()
        ctk.CTkLabel(self.current_frame, text="Fonctionnalité en cours de rendu optimisé...").pack(pady=20)

    def show_finances(self):
        self.clear_frame()
        # Vue pour les paiements
        pass

if __name__ == "__main__":
    app = GestLocApp()
    app.mainloop()