import customtkinter as ctk
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


    ctk.CTkButton(app, text='Suivant', command=go_to_info).place(x=350, y=320)
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

    button_new_loc = ctk.CTkButton(app, text="Enregistrement des nouveaux locataire", command=lambda: (app.destroy()))
    button_new_loc.pack(pady=20)
    
    button_afficher_loc = ctk.CTkButton(app, text="Afficher les locataires", command=lambda: (app.destroy()))
    button_afficher_loc.pack(pady=20)
    
    button_retour = ctk.CTkButton(app, text="Paiment des loyer", command=lambda: (app.destroy()))
    button_retour.pack(pady=20)
    button_loyers = ctk.CTkButton(
    app,
    text="Afficher les paiements reçus",
    command=lambda: (app.destroy())
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

    # Bouton Gestion des appartements
    button = ctk.CTkButton(app, text='Gestion des appartements', width=200, height=45)
    button.place(x=300, y=150)

    # Bouton Gestion des locataires
    button2 = ctk.CTkButton(app, text='Gestion des locataires', width=200, height=45, command=lambda: (app.destroy(), Locataire()))
    button2.place(x=300, y=250)

    app.mainloop()

# ==========================
# LANCEMENT APPLICATION
# ==========================
Principale()