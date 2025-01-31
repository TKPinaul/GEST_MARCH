from rich import print as rprint
from rich.console import Console
from rich.table import Table

from GEST_MARCH.models.marche import Marche
from GEST_MARCH.utils.afficher_menu import marche_menu


def table_title():
   table = Table(title="Information du marché")
   table.add_column("ID", style="green", no_wrap=True)
   table.add_column("NOM", style="blue")
   table.add_column("Matrice", style="cyan")
   return table
   
def gestion_marche():
   console = Console()
   
   while True:
      marche_menu()
      choix = input("Choisisser une option: ")
      
      if choix == "1": # Créer un marché
         nom_marche = input("Entrez le nom du marché: ")
         # en absence de coordonne X*Y nous prendrons 50*50
         x_ligne = int(input("Entrez le nombre de ligne: "))
         y_colonne = int(input("Entrez le nombre de ligne: "))
         marche = Marche(nom_marche, x_ligne, y_colonne)
         marche.save() # Création du marché
         rprint('[green]Marché créé avec succès![/green]')
         
      elif choix == "2": # Afficher tous les marchés
         marches = Marche.get_all()
         table = table_title()
         for marche_data in marches:
            marche = Marche.from_dict(marche_data)
            table.add_row(
               str(marche.marche_id),
               marche.nom_marche,
               f"{marche.x_ligne}X{marche.y_colonne}"
            )
         console.print(table)
         
      elif choix == "3": # Afficher un marché
         marche_id = input("Entrez l'ID du marché : ")
         marche_data = Marche.get_one(marche_id)
         if marche_data:
            marche = Marche.from_dict(marche_data)
            table = table_title()
            table.add_row(
               marche.marche_id,
               marche.nom_marche,
               f"{marche.x_ligne}X{marche.y_colonne}"
            )
            console.print(table)
         else:
            rprint("[red]Marché non trouvé[/red]")
      
      elif choix == "4": # Afficher les stands d'un marché
         marche_id = input("Entrez l'ID du marché : ")
         marche_data = Marche.get_one(marche_id)
         if marche_data:
            marche = Marche.from_dict(marche_data)
            table = Table(title=f"Affichage des Stand du marché {marche.nom_marche}")
            for i in range(marche.x_ligne):
               row = []
               for j in range(marche.y_colonne):
                  etat_stand = 'X' if marche.grille[i][j] else 'O'
                  row.append(etat_stand)
                  table.add_row(
                     " ".join(row)
                  )
            console.print(table)
         else:
            rprint("[red]Marché non trouvé[/red]")
         
      elif choix == "5":
         break
      else:
         rprint("[red]Option invalide, Veuillez réessayer[/red]")
      