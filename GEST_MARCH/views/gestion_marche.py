from rich import print as rprint
from rich.console import Console
from GEST_MARCH.models.marche import Marche
from GEST_MARCH.utils.afficher_menu import marche_menu
from GEST_MARCH.utils.table_titre import table_marche_title, table_stand_title

   
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
         
         if not marches:
            console.print("[bold red]Aucun marché disponible.[/bold red]", style="bold")
            continue
         
         table = table_marche_title()
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
            table = table_marche_title()
            table.add_row(
               marche.marche_id,
               marche.nom_marche,
               f"{marche.x_ligne}X{marche.y_colonne}"
            )
            console.print(table)
         else:
            rprint("[red]Marché non trouvé[/red]")
      
      elif choix == "4": # Afficher les stands d'un marché
         marche_id = input("Entrez l'ID du marché: ")
         marche_data = Marche.get_one(marche_id)
         if not marche_data:
            console.print("[bold red]ID du marché incorrect.[/bold red]", style="bold")
            continue
         
         marche = Marche.from_dict(marche_data)
         table = table_stand_title(marche.nom_marche)
         for x in range(marche.x_ligne):
            for y in range(marche.y_colonne):
               statut = "Occupé" if marche.grille[x][y] else "Libre"
               table.add_row(f"({x}, {y})", statut)
         console.print(table)
         
      elif choix == "5":
         console.print("[bold yellow]Merci d'avoir consulté notre service![/bold yellow]", style="bold")
         break
      
      else:
         rprint("[red]Option invalide, Veuillez réessayer[/red]")
      