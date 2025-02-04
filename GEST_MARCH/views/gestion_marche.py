import uuid
from rich import print as rprint
from rich.console import Console
from GEST_MARCH.models.marche import Marche
from GEST_MARCH.utils.afficher_menu import marche_menu
from GEST_MARCH.utils.afficher_stand import afficher_marche
from GEST_MARCH.utils.fonction_util import demander_entier
from GEST_MARCH.utils.table_titre import table_marche_title, table_stand_title

   
def gestion_marche():
   console = Console()
   
   while True:
      marche_menu()
      choix = input("Choisisser une option: ")
      
      if choix == "0": # Afficher tous les marchés
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
         
      elif choix == "1": # Afficher un marché
         marche_id = input("Entrez l'ID du marché : ").strip()
         try:
            uuid.UUID(marche_id) # verifier la validite de l'id
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
         except ValueError:
            rprint("[red]ID du marché est invalide. Veuillez entrer id valide (consulter option 0!).[/red]")
             
      elif choix == "2": # Afficher les stands d'un marché
         marche_id = input("Entrez l'ID du marché: ").strip()
         try:
            uuid.UUID(marche_id)
            
            marche_data = Marche.get_one(marche_id)
            if not marche_data:
               console.print("[bold red]ID du marché incorrect.[/bold red]", style="bold")
               continue
         
            marche = Marche.from_dict(marche_data)
            afficher_marche(marche)
         except ValueError:
            rprint("[red]ID du marché est invalide. Veuillez entrer id valide (consulter option 0!).[/red]")
         
      elif choix == "3": # Quitter
         console.print("[bold yellow]Merci d'avoir consulté notre service![/bold yellow]", style="bold")
         break
      
      else:
         rprint("[red]Option invalide, Veuillez réessayer[/red]")
      