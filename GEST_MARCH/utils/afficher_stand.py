import matplotlib.pyplot as plt

def afficher_marche(marche):
   fig, ax = plt.subplots(figsize=(5, 5)) # cration de la figure
   
   for x in range(marche.x_ligne): # Parcour les ligne
      for y in range(marche.y_colonne): # Parcour les colonnes
         if marche.grille[x][y]: # stand occupé
            ax.plot(y, x, 'go', markersize=8, label='Occupé' if not any(l.get_label() == "Occupé" for l in ax.get_lines()) else "")
         else: # stand libre
            ax.plot(y, x, 'ro', markersize=8, label='Libre' if not any(l.get_label() == "Libre" for l in ax.get_lines()) else "")
   
   # Configuration du repère
   ax.set_xlabel("Colonne (y)")
   ax.set_ylabel("Ligne (x)")
   ax.set_xlim(-1, marche.y_colonne)
   ax.set_ylim(-1, marche.x_ligne)
   ax.set_xticks(range(marche.y_colonne))
   ax.set_yticks(range(marche.x_ligne))
   ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
   
   plt.title(f"Présentation du {marche.nom_marche} ({marche.x_ligne}X{marche.y_colonne})") # Affichage du titre de la figure
   plt.legend() # Affichage des légendes
   
   plt.show() # Affichage de la figure