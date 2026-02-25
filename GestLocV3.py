import customtkinter as ctk

# ==========================
# PAGE INFO APPARTEMENTS PAR NIVEAU (Nouveau en V3)
# ==========================
def InfoAppart(nb_niv):
    app = ctk.CTk()
    app.title("GesLoc - Configuration")
    app.geometry("800x600+400+50")
    app.resizable(False, False)

    label = ctk.CTkLabel(app, text="Nombre d'appartements par niveau", font=('Arial Black', 16))
    label.pack(pady=20)
    
    frame_rez = ctk.CTkFrame(app)
    frame_rez.pack(pady=10)

    ctk.CTkLabel(frame_rez, text="Rez de chaussée :", font=('Arial Narrow', 14)).pack(side="left", padx=10)
    entry_rez = ctk.CTkEntry(frame_rez, placeholder_text="Nombre d'apparts")
    entry_rez.pack(side="left", padx=10)

    # Création dynamique des champs pour les étages
    entries = []
    for i in range(nb_niv):
        frame = ctk.CTkFrame(app)
        frame.pack(pady=10)
        ctk.CTkLabel(frame, text=f"Niveau {i+1} :", font=('Arial Narrow', 14)).pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame, placeholder_text=f"Nombre d'apparts")
        entry.pack(side="left", padx=10)
        entries.append(entry)

    def go_next():
        # Pour l'instant, on détruit juste la fenêtre (la logique V4 viendra après)
        print("Configuration des niveaux terminée.")
        app.destroy()
        Principale()

    ctk.CTkButton(app, text="Suivant", command=go_next).pack(pady=20)
    app.mainloop()

# ==========================
# PAGE APPARTEMENT (Améliorée en V3)
# ==========================
def Appartement():
    app = ctk.CTk()
    app.title("GesLoc - Immeuble")
    app.geometry("800x600+400+50")
    app.resizable(False, False)

    ctk.CTkLabel(app, text="Information sur l'immeuble", font=('Arial Black', 16)).place(x=280, y=10)
    
    # Champs de saisie
    ctk.CTkLabel(app, text="Adresse de l'immeuble :").place(x=10, y=50)
    zone1 = ctk.CTkEntry(app, width=300)
    zone1.place(x=250, y=50)

    ctk.CTkLabel(app, text="Nombre de niveaux :").place(x=10, y=100)
    zone2 = ctk.CTkEntry(app, placeholder_text="Ex: 2")
    zone2.place(x=250, y=100)

    ctk.CTkLabel(app, text="Prix du m2 ($):").place(x=10, y=150)
    zone3 = ctk.CTkEntry(app)
    zone3.place(x=250, y=150)

    ctk.CTkLabel(app, text="Nom du propriétaire :").place(x=10, y=200)
    zone4 = ctk.CTkEntry(app, width=300)
    zone4.place(x=250, y=200)

    def valider_et_continuer():
        try:
            niveaux = int(zone2.get())
            app.destroy()
            InfoAppart(niveaux) # On passe à la fenêtre suivante
        except:
            print("Erreur : Entrez un nombre de niveaux valide.")

    ctk.CTkButton(app, text='Suivant', command=valider_et_continuer).place(x=350, y=320)
    app.mainloop()

# ==========================
# PAGE LOCATAIRE (Inchangée)
# ==========================
def Locataire():
    app = ctk.CTk()
    app.title("GesLoc - Locataires")
    app.geometry("800x600+400+50")
    app.pack_propagate(False)
    
    ctk.CTkLabel(app, text="Menu Locataires", font=('Arial Black', 16)).pack(pady=20)
    ctk.CTkButton(app, text="Retour", command=lambda: (app.destroy(), Principale())).pack()
    app.mainloop()

# ==========================
# PAGE PRINCIPALE
# ==========================
def Principale():
    app = ctk.CTk()
    app.title("GesLoc")
    app.geometry("800x600+400+50")

    ctk.CTkLabel(app, text='GEST LOC APP', font=('Arial Black', 20)).place(x=300, y=50)

    ctk.CTkButton(app, text='Gestion des appartements', width=200, command=lambda: (app.destroy(), Appartement())).place(x=300, y=150)
    ctk.CTkButton(app, text='Gestion des locataires', width=200, command=lambda: (app.destroy(), Locataire())).place(x=300, y=250)

    app.mainloop()

Principale()