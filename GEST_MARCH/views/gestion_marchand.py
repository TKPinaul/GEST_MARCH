from rich import print as rprint
from rich.console import Console
from GEST_MARCH.models.marchands import Marchands
from GEST_MARCH.models.marche import Marche
from GEST_MARCH.utils.afficher_menu import marchand_menu
from GEST_MARCH.utils.table_titre import table_marchand_title, table_marche_title, table_stand_title
   

def gestion_marchand():
   console = Console()
   
   while True:
      marchand_menu()
      choix = input("Choisisser une option: ")
      
      if choix == "1": # Afficher tous les marchés
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
      
      elif choix == "2": # Afficher les stand d'un marché
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
         
      elif choix == "3": # Créer un marchand
         try:
            nom = input("Entrez le nom du marchand: ")
            contact = input("Entrez le contact du marchand: ")
            coordonneeX = int(input("Entrez la coordonnée X: "))
            coordonneeY = int(input("Entrez la coordonnée Y: "))
            marche_id = input("Entrez l'ID du marché où le marchand sera installé: ")
            
            stock = {} # initialisation du stock
            response = input("Ajouter du stock ? (O/N): ").strip().upper()
            while response == "O":
               produit = input("Entrez le nom du produits: ").strip()
               quantite = int(input("Quantiter totale a enregistrer: "))
               prix_unitaire = float(input("Quel est le prix unitaire de ce produits: "))
               
               stock[produit] = {
                  'quantite': quantite,
                  'prix_unitaire': prix_unitaire
               } # Ajout du produitts au stock
               response = input("Ajouter un autre produit ? (O/N): ").strip().upper()
            
            
            marche_data = Marche.get_one(marche_id) # recupération du marché par son ID
            if not marche_data: # Vérifi si le marché a été récupéré
               console.print("[bold red]Marché non trouvé, veuiller consulter le choix '1'.[/bold red]", style="bold")
               continue
            
            marche = Marche.from_dict(marche_data) # Créer une instance de Marche à partir des données récupérées
            
            # verification de la disponibilite du stand
            if not marche.stand_available(coordonneeX, coordonneeY):
               console.print(f"[bold red]Le stand ({coordonneeX}, {coordonneeY}) est déjà occupé ou hors de la grille.[/bold red]", style="bold")
               continue
            
            marchand = Marchands(
               nom=nom,
               contact=contact,
               coordonneeX=coordonneeX,
               coordonneeY=coordonneeY,
               stock=stock
            )
            marchand.save(marche_id) # Enregistrement du marchand
            console.print("[bold green]Marchand créé avec succès![/bold green]", style="bold")

         except ValueError as e:
            console.print(f"[bold red]Erreur: {e}[/bold red]", style="bold")
         except Exception as e:
            console.print(f"[bold red]Erreur inattendue : {e}[/bold red]", style="bold")
            
      elif choix == "4": # Afficher tous les marchands
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
            
            stock_list = []
            for produit, details in marchand.get('stock', {}).items():
               stock_list.append(f"{produit} | {details['quantite']} | {details['prix_unitaire']:.2f}")

            stock_display = "\n".join(stock_list) if stock_list else "Aucun produit"
            
            table.add_row(
               marchand['code_id'],
               marchand['nom'],
               marchand['contact'],
               marchand['type_personne'],
               f"({marchand['coordonneeX']}, {marchand['coordonneeY']})",
               nom_marche,
               stock_display
            )
         console.print(table)
          
      elif choix == "5": # Afficher les informations d'un marchand
         code_id = input("Entrez l'ID du marchand: ")
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
         
         stock_list = []
         for produit, details in marchand.get('stock', {}).items():
            stock_list.append(f"{produit} | {details['quantite']} | {details['prix_unitaire']:.2f}")

         stock_display = "\n".join(stock_list) if stock_list else "Aucun produit"
            
         table = table_marchand_title()
         table.add_row(
            marchand['code_id'],
            marchand['nom'],
            marchand['contact'],
            marchand['type_personne'],
            f"({marchand['coordonneeX']}, {marchand['coordonneeY']})",
            nom_marche,
            stock_display
         )
         console.print(table)
         
      elif choix == "6": # Modifier les informations d'un marchand
         code_id = input("Entrez l'ID du marchand à modifier: ")
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
            
      elif choix == "7": # Supprimer un marchand
         code_id = input("Entrez l'ID du marchand à supprimer: ")
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
         
      elif choix == "8": # Quitter
         console.print("[bold yellow]Merci d'avoir consulté notre service![/bold yellow]", style="bold")
         break
      
      else:
         rprint("[bold red]Option invalide, veuillez réessayer.[/bold red]", style="bold")
         