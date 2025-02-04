import uuid
from rich import print as rprint
from rich.console import Console
from GEST_MARCH.models.marchands import Marchands
from GEST_MARCH.models.marche import Marche
from GEST_MARCH.utils.afficher_menu import marchand_menu
from GEST_MARCH.utils.afficher_stand import afficher_marche
from GEST_MARCH.utils.fonction_util import demander_entier
from GEST_MARCH.utils.table_titre import table_marchand_title, table_marche_title, table_stand_title, table_stock_title
   

def gestion_marchand():
   console = Console()
   
   while True:
      marchand_menu()
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
      
      elif choix == "1": # Afficher les stand d'un marché
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
            rprint("[red]ID du marché est invalide. Veuillez entrer id valide (consulter option 2!).[/red]")
  
      elif choix == "2": # Afficher tous les marchands
         marchands = Marchands.get_all()
         
         if not marchands:
            console.print("[bold red]Aucun marchand trouvé.[/bold red]", style="bold")
            continue
         
         table = table_marchand_title()
         for marchand in marchands:
            if not isinstance(marchand, dict):
               console.print("[bold red]Données de marchand invalides.[/bold red]", style="bold")
               continue

            marche_id = marchand.get('marche_id')
            nom_marche = "N/A"  # Valeur par défaut si le marché n'est pas trouvé
            
            if marche_id:
               marche_data = Marche.get_one(marche_id)
               if marche_data:
                  marche = Marche.from_dict(marche_data)
                  nom_marche = marche.nom_marche
            
            table.add_row(
               marchand['code_id'],
               marchand['nom'],
               marchand['contact'],
               marchand['type_personne'],
               f"({marchand['coordonneeX']}, {marchand['coordonneeY']})",
               nom_marche
            )
         console.print(table)
          
      elif choix == "3": # Afficher les informations d'un marchand
         code_id = input("Entrez l'ID du marchand: ").strip()
         try:
            uuid.UUID(code_id)
            marchand = Marchands.get_one(code_id)
            
            if not marchand:
               console.print("[bold red]ID du marchand invalid[/bold red]", style="bold")
               continue
            
            marche_id = marchand.get('marche_id')
            nom_marche = "N/A"  # Valeur par défaut si le marché n'est pas trouvé
            
            if marche_id:
               marche_data = Marche.get_one(marche_id)
               if marche_data:
                  marche = Marche.from_dict(marche_data)
                  nom_marche = marche.nom_marche
            
            table = table_marchand_title()
            table.add_row(
               marchand['code_id'],
               marchand['nom'],
               marchand['contact'],
               marchand['type_personne'],
               f"({marchand['coordonneeX']}, {marchand['coordonneeY']})",
               nom_marche
            )
            console.print(table)
            
         except ValueError:
            rprint("[red]ID du marchand est invalide. Veuillez entrer un id valide (consulter option 2!).[/red]")
            
      elif choix == "4": # Afficher les stock d'un marchand
         code_id = input("Entrez l'ID du marchand: ").strip()
         try:
            uuid.UUID(code_id)
            marchand = Marchands.get_one(code_id)
            if not marchand:
               console.print("[bold red]ID du marchand invalid[/bold red]", style="bold")
               continue
            
            stock = marchand.get("stock", {})
            if not stock:
               console.print(f"[bold yellow]Le marchand {marchand['nom']} n'a pas de stock enregistré.[/bold yellow]", style="bold")
               continue
               
            table = table_stock_title(marchand['nom'])
            for produit, details in stock.items():
               table.add_row(
                  produit,
                  str(details.get("quantite", "N/A")),  # Sécurisation des valeurs
                  f"{details.get('prix_unitaire', 'N/A'):.2f} €"
               )
            console.print(table)
            
         except ValueError:
            rprint("[red]ID du marchand est invalide. Veuillez entrer un id valide (consulter option 2!).[/red]")
      
      elif choix == "5": # Modifier les informations d'un marchand
         code_id = input("Entrez l'ID du marchand à modifier: ").strip()
         
         try:
            uuid.UUID(code_id)
            new_nom = input("Entrez le nouveau nom (laissez vide pour ne pas changer): ")
            new_contact = input("Entrez le nouveau contact (laissez vide pour ne pas changer): ")
            marchand_data = Marchands.get_one(code_id)
            if not marchand_data:
               console.print("[bold red]ID du marchand invalid[/bold red]", style="bold")
               continue
            
            marchand = Marchands.from_dict(marchand_data)
            try:
               if new_nom:
                  marchand.nom = new_nom
               if new_contact:
                  marchand.contact = new_contact
               marchand.update_personne('marchands', new_nom, new_contact)
               console.print("[bold green]Marchand modifié avec succès![/bold green]", style="bold")
            except Exception as e:
               console.print(f"[bold red]Erreur: {e}[/bold red]", style="bold")
         
         except ValueError:
            rprint("[red]ID du marchAND est invalide. Veuillez entrer id valide (consulter option 4!).[/red]")
            
      elif choix == "6": # Supprimer un marchand
         code_id = input("Entrez l'ID du marchand à supprimer: ").strip
         marchand_data = Marchands.get_one(code_id)
         
         if not marchand_data:
            console.print("[bold red]ID du marchand invalid[/bold red]", style="bold")
            continue
         
         marche_id = marchand_data['marche_id']
         if not marche_id:
            console.print("[bold red]Marché associé non trouvé.[/bold red]", style="bold")
            continue
         
         marche_data = Marche.get_one(marche_id)
         if not marche_data:
            console.print("[bold red]Marché associé non trouvé.[/bold red]", style="bold")
            continue
         
         marche = Marche.from_dict(marche_data)
         marchand = Marchands.from_dict(marchand_data)
         try:
            marchand.delete_marchand(marche)
            console.print("[bold green]Marchand supprimé avec succès![/bold green]", style="bold")
         except Exception as e:
            console.print(f"[bold red]Erreur: {e}[/bold red]", style="bold")
         
      elif choix == "7": # Quitter
         console.print("[bold yellow]Merci d'avoir consulté notre service![/bold yellow]", style="bold")
         break
      
      else:
         rprint("[bold red]Option invalide, veuillez réessayer.[/bold red]", style="bold")
         