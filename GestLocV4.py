import customtkinter as ctk

# ==================================
# PAGE DIMENSIONS DES PIECES (Nouveau V4)
# ==================================
def DimensionsPieces(pieces_data):
    app = ctk.CTk()
    app.title("GesLoc - Dimensions")
    app.geometry("900x700+100+20")
    app.resizable(False, False)

    ctk.CTkLabel(app, text="Dimensions des pièces (m²)", font=('Arial Black', 16)).pack(pady=20)

    # Utilisation d'un cadre défilant pour gérer beaucoup de pièces
    scroll_frame = ctk.CTkScrollableFrame(app, width=850, height=500)
    scroll_frame.pack(pady=10)

    for niveau, appartements in pieces_data.items():
        frame_niveau = ctk.CTkFrame(scroll_frame)
        frame_niveau.pack(pady=10, fill="x", padx=10)

        ctk.CTkLabel(frame_niveau, text=f"Niveau : {niveau}", font=('Arial Black', 14)).pack(anchor="w", pady=5)

        for appart_index, nb_pieces in enumerate(appartements, start=1):
            frame_app = ctk.CTkFrame(frame_niveau)
            frame_app.pack(pady=5, fill="x", padx=20)
            ctk.CTkLabel(frame_app, text=f"Appartement {appart_index}", font=('Arial Narrow', 13)).pack(anchor="w")

            for p in range(1, nb_pieces + 1):
                frame_p = ctk.CTkFrame(frame_app)
                frame_p.pack(pady=2, fill="x", padx=30)
                ctk.CTkLabel(frame_p, text=f"Surface Pièce {p} :").pack(side="left", padx=10)
                ctk.CTkEntry(frame_p, placeholder_text="m²").pack(side="left", padx=10)

    ctk.CTkButton(app, text="Terminer", command=lambda: (app.destroy(), Principale())).pack(pady=10)
    app.mainloop()

# ======================================
# PAGE NOMBRE DE PIECES / APPART (Nouveau V4)
# ======================================
def NbPiecesParAppartement(apparts_par_niveau):
    app = ctk.CTk()
    app.title("GesLoc - Détails Appartements")
    app.geometry("800x650+200+20")

    ctk.CTkLabel(app, text="Nombre de pièces par appartement", font=('Arial Black', 16)).pack(pady=20)
    scroll_frame = ctk.CTkScrollableFrame(app, width=750, height=450)
    scroll_frame.pack()

    all_entries = {}

    for index, nb_apparts in enumerate(apparts_par_niveau):
        nom_niv = "Rez-de-chaussée" if index == 0 else f"Niveau {index}"
        
        frame_niv = ctk.CTkFrame(scroll_frame)
        frame_niv.pack(pady=10, fill="x")
        ctk.CTkLabel(frame_niv, text=nom_niv, font=('Arial Black', 14)).pack(anchor="w")

        entries_du_niveau = []
        for a in range(1, nb_apparts + 1):
            f = ctk.CTkFrame(frame_niv)
            f.pack(pady=5, padx=20)
            ctk.CTkLabel(f, text=f"Appartement {a} :").pack(side="left", padx=10)
            ent = ctk.CTkEntry(f, placeholder_text="Nb pièces")
            ent.pack(side="left", padx=10)
            entries_du_niveau.append(ent)
        
        all_entries[nom_niv] = entries_du_niveau

    def vers_dimensions():
        # Simulation de la récupération des données pour la fenêtre suivante
        pieces_data = {}
        for niv, entry_list in all_entries.items():
            pieces_data[niv] = [int(e.get() if e.get() else 0) for e in entry_list]
        app.destroy()
        DimensionsPieces(pieces_data)

    ctk.CTkButton(app, text="Suivant", command=vers_dimensions).pack(pady=20)
    app.mainloop()

# ==================================
# PAGE INFO APPART (Mise à jour V4)
#