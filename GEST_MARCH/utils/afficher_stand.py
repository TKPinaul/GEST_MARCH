import matplotlib.pyplot as plt

from configs.bd_connexion import get_database

def afficher_marche(marche):
   fig, ax = plt.subplots(figsize=(6, 6)) # cration de la figure
   
   # Récupérer tous les marchands associés à ce marché
   db = get_database()
   collection = db['marchands']
   marchands = list(collection.find({'marche_id': marche.marche_id}))
   
   for x in range(marche.x_ligne): # Parcour les ligne
      for y in range(marche.y_colonne): # Parcour les colonnes
         if marche.grille[x][y]: # stand occupé
            # Trouver le marchand correspondant à ce stand
            marchand = next((m for m in marchands if m['coordonneeX'] == x and m['coordonneeY'] == y), None)
            if marchand:
               ax.plot(x, y, 'go', markersize=8, label='Occupé' if not any(l.get_label() == "Occupé" for l in ax.get_lines()) else "")
               ax.text(x, y + 0.2, marchand['nom'], fontsize=10, ha='center', va='bottom', color='darkblue')
         else: # stand libre
            ax.plot(x, y, 'ro', markersize=8, label='Libre' if not any(l.get_label() == "Libre" for l in ax.get_lines()) else "")
   
   # Configuration du repère
   ax.set_xlabel("Coordonnée X", fontsize=12, weight='bold')
   ax.set_ylabel("Coordonnée Y", fontsize=12, weight='bold')
   ax.set_xlim(-1, marche.x_ligne)
   ax.set_ylim(-1, marche.y_colonne)
   ax.set_xticks(range(marche.x_ligne))
   ax.set_yticks(range(marche.y_colonne))
   ax.grid(True, linestyle='--', linewidth=0.7, alpha=0.7, color='w')
   
   plt.title(f"Présentation du {marche.nom_marche} ({marche.x_ligne}X{marche.y_colonne})", fontsize=14, weight='bold', pad=20) # Affichage du titre de la figure
   plt.legend() # Affichage des légendes
   
   ax.set_facecolor('white')
   fig.patch.set_facecolor('lavender')  # Couleur de fond de la figure
   plt.tight_layout()  # Ajuster l'espacement
   
   plt.show() # Affichage de la figure