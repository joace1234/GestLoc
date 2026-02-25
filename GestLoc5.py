import customtkinter as ctk

# ==================================
# FORMULAIRE NOUVEAU LOCATAIRE (Nouveau V5)
# ==================================
def NewLoc():
    app = ctk.CTk()
    app.title("GesLoc - Nouveau Locataire")
    app.geometry("800x650+400+50")
    app.resizable(False, False)

    ctk.CTkLabel(app, text="Enregistrement d'un nouveau locataire", font=('Arial Black', 18)).pack(pady=20)

    # Conteneur pour le formulaire
    form_frame = ctk.CTkFrame(app, width=700, height=450)
    form_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Champs de saisie
    fields = [
        ("Nom :", "Entrez le nom"),
        ("Postnom :", "Entrez le postnom"),
        ("Prénom :", "Entrez le prénom"),
        ("Lieu et Date de Naissance :", "Ex: Kinshasa, 01/01/1990"),
        ("Taille de la famille :", "Nombre de personnes"),
        ("Date d'entrée :", "JJ/MM/AAAA")
    ]

    entries = {}
    for label_text, placeholder in fields:
        row = ctk.CTkFrame(form_frame, fg_color="transparent")
        row.pack(fill="x", padx=50, pady=10)
        ctk.CTkLabel(row, text=label_text, width=200, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(row, placeholder_text=placeholder, width=300)
        entry.pack(side="right")
        entries[label_text] = entry

    # Sélection Immeuble/Appart (Simulée pour l'instant)
    row_selection = ctk.CTkFrame(form_frame, fg_color="transparent")
    row_selection.pack(fill="x", padx=50, pady=10)
    
    ctk.CTkLabel(row_selection, text="Attribuer Appartement :", width=200, anchor="w").pack(side="left")
    ctk.CTkOptionMenu(row_selection, values=["Choisir Immeuble..."], width=145).pack(side="left", padx=5)
    ctk.CTkOptionMenu(row_selection, values=["Appartement..."], width=145).pack(side="left")

    def sauvegarder():
        # Logique de validation simple
        print(f"Locataire {entries['Nom :'].get()} enregistré (Localement) !")
        app.destroy()
        Locataire()

    ctk.CTkButton(app, text="Enregistrer le locataire", fg_color="green", hover_color="darkgreen", 
                  command=sauvegarder).pack(pady=20)
    
    ctk.CTkButton(app, text="Annuler", fg_color="red", command=lambda: (app.destroy(), Locataire())).pack(pady=5)
    
    app.mainloop()

# ==================================
# MENU LOCATAIRE (Mise à jour V5)
# ==================================
def Locataire():
    app = ctk.CTk()
    app.title("GesLoc - Gestion Locataires")
    app.geometry("800x600+400+50")

    ctk.CTkLabel(app, text="Menu de Gestion des Locataires", font=('Arial Black', 18)).pack(pady=40)

    # Boutons d'action
    ctk.CTkButton(app, text="➕ Ajouter un Locataire", width=250, height=50, 
                  command=lambda: (app.destroy(), NewLoc())).pack(pady=15)
    
    ctk.CTkButton(app, text="📋 Liste des Locataires", width=250, height=50, 
                  command=lambda: print("Indisponible en V5")).pack(pady=15)
    
    ctk.CTkButton(app, text="💰 Enregistrer un Paiement", width=250, height=50,
                  command=lambda: print("Indisponible en V5")).pack(pady=15)

    ctk.CTkButton(app, text="⬅ Retour au Menu Principal", width=200, fg_color="gray",
                  command=lambda: (app.destroy(), Principale())).pack(pady=30)

    app.mainloop()

# ==================================
# PAGE PRINCIPALE (Inchangée mais connectée)
# ==================================
def Principale():
    app = ctk.CTk()
    app.title("GesLoc")
    app.geometry("800x600+400+50")

    ctk.CTkLabel(app, text='GEST LOC APP', font=('Arial Black', 20)).pack(pady=50)

    ctk.CTkButton(app, text='Gestion des appartements', width=200, height=45,
                  command=lambda: print("Voir V4 pour cette partie")).pack(pady=10)
    
    ctk.CTkButton(app, text='Gestion des locataires', width=200, height=45, 
                  command=lambda: (app.destroy(), Locataire())).pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    Principale()