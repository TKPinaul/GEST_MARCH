import uuid
from rich import print as rprint
from rich.console import Console

from GEST_MARCH.models.marchands import Marchands
from GEST_MARCH.models.marche import Marche
from GEST_MARCH.models.transactionClient import TransactionClient
from GEST_MARCH.utils.afficher_menu import client_menu
from GEST_MARCH.utils.fonction_util import demander_entier
from GEST_MARCH.utils.table_titre import table_marchand_title, table_panier_title, table_stock_title


def gestion_transaction_client():
   console = Console()
   
   while True:
      client_menu()
      choix = input("Choisissez une option: ")
      
      if choix == "0": # Afficher tous les marchands
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
         
      elif choix == "1": # Afficher les produits d'un marchants
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
            rprint("[red]ID du marchand est invalide. Veuillez entrer un id valide (consulter option 0!).[/red]")
         
      elif choix == "2": # Rechercher une liste de produit
         paniers = []
         continuer = True
         rprint("[blue]Veuillez remplir le panier des produits que vous cherchez (1 a 1).[/blue]")
         while continuer:
            produit = input("Produit cherché : ").strip().capitalize()
            paniers.append(produit)
            reponse = input("Voulez-vous ajouter un autre produit ? (O/N) : ").strip().upper()
            
            if reponse != "O":
               continuer = False
         
         if not paniers:
            rprint("[bold red]Aucun produit n'a été saisi pour la recherche.[/bold red]", style="bold")
         
         resultats = Marchands.recherche_produits(paniers)
         
         # Liste des produits trouvés
         produits_trouves = {produit["nom_produit"] for resultat in resultats for produit in resultat["produits"]}

         # Identifier les produits introuvables
         produits_introuvables = set(paniers) - produits_trouves
         
         
         if not resultats:
            rprint("[bold yellow]Aucun produit trouvé dans les stocks des marchands.[/bold yellow]", style="bold")
            continue
         
         table = table_panier_title()
         for resultat in resultats:
            marchand_data = Marchands.get_one(resultat["code_marchand"])
            
            if not marchand_data:
               continue
            
            marchand = Marchands.from_dict(marchand_data)
            stand = f"({marchand.coordonneeX}, {marchand.coordonneeY})"
            
            marche_id = marchand_data.get("marche_id")
            nom_marche = "N/A" # Valeur par défaut si le marché n'est pas trouvé
            if marche_id:
               marche_data = Marche.get_one(marche_id)
               if marche_data:
                  marche = Marche.from_dict(marche_data)
                  nom_marche = marche.nom_marche
            
            for produit in resultat["produits"]:
               table.add_row(
                  resultat["code_marchand"],
                  marchand.nom,
                  stand,
                  produit["nom_produit"],
                  str(produit["quantite"]),
                  f"{produit['prix_unitaire']} €",
                  nom_marche
               )
         console.print(table)
         # Afficher un message si certains produits n'ont pas été trouvés
         if produits_introuvables:
            rprint(f"[bold red]Les produits suivants n'ont pas été trouvés : {', '.join(produits_introuvables)}[/bold red]")
         
      elif choix == "3": # Acheter un produit
         code_marchand = input("Entrez l'ID du marchand: ").strip()
         
         try:
            uuid.UUID(code_marchand)
            
            code_client = input("Entrez l'ID du client: ").strip()
            try:
               uuid.UUID(code_client)
               nom_produit = input("Entrez le nom du produit: ").strip()
               quantite_achetee = demander_entier("Entrez la quantité: ")
               marchand_data = Marchands.get_one(code_marchand)
               if not marchand_data:
                  console.print("[bold red]ID du marchand invalide.[/bold red]", style="bold")
                  continue
               
               marchand = Marchands.from_dict(marchand_data)
               
               stock = marchand.stock
               if nom_produit not in stock:
                  console.print(f"[bold red]Le produit '{nom_produit}' n'est pas disponible chez ce marchand.[/bold red]", style="bold")
                  continue
               
               quantite_disponible = stock[nom_produit]["quantite"]
               if quantite_achetee > quantite_disponible:
                  console.print(f"[bold red]Quantité insuffisante. Seulement {quantite_disponible} unités disponibles.[/bold red]", style="bold")
                  continue
               
               prix_unitaire = stock[nom_produit]["prix_unitaire"]
               montant_total = prix_unitaire * quantite_achetee
               
               nouvelle_quantite = quantite_disponible - quantite_achetee
               marchand.update_quantite(nom_produit, nouvelle_quantite)
               transaction = TransactionClient(
                  code_client=code_client,
                  code_marchand=code_marchand,
                  nom_produit=nom_produit,
                  quantite_achetee=quantite_achetee,
                  prix_unitaire=prix_unitaire
               )
               transaction.save_transaction()
               console.print("[bold green]Transaction enregistrée avec succès ![/bold green]", style="bold")
               console.print(f"Produit : {nom_produit}", style="bold")
               console.print(f"Quantité achetée : {quantite_achetee}", style="bold")
               console.print(f"Montant total : {montant_total:.2f} €", style="bold")
            except ValueError:
               console.print(f"[bold red]ID du client est invalide (connecter vous comme admin pour voir l'id du client).")
         except ValueError:
            console.print(f"[bold red]ID du marchand est invalide. Veuillez entrer id valide (consulter option 1!).")
         except Exception as e:
            console.print(f"[bold red]Une erreur s'est produite : {e}[/bold red]", style="bold")
            
      elif choix == "4":  
         console.print("[bold yellow]Merci d'avoir consulté notre service![/bold yellow]", style="bold")
         break
      
      else:
         rprint("[bold yellow]Option invalide, veuillez réessayer.[/bold yellow]")
