import customtkinter as ctk


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
    
    # Bouton Gestion des appartements
    button = ctk.CTkButton(app, text='Gestion des appartements', width=200, height=45)
    button.place(x=300, y=150)

    # Bouton Gestion des locataires
    button2 = ctk.CTkButton(app, text='Gestion des locataires', width=200, height=45, )
    button2.place(x=300, y=250)

    app.mainloop()

# ==========================
# LANCEMENT APPLICATION
# ==========================
Principale()