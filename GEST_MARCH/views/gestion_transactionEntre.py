from rich import print as rprint
from rich.console import Console
from GEST_MARCH.models.marchands import Marchands
from GEST_MARCH.models.marche import Marche
from GEST_MARCH.models.transactionEntre import TransactionEntree
from GEST_MARCH.utils.afficher_menu import transactionEntre_menu
from GEST_MARCH.utils.table_titre import table_marchand_title, table_transactionEntre_title


def gestion_transaction_entree():
   console = Console()
   
   while True:
      transactionEntre_menu()
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

      elif choix == "1": # Ravitaillement de stock d'un produit
         code_marchand = input("Entrez l'ID du marchand: ")
         nom_produit = input("Entrez le nom du produit: ")
         quantite_entree = int(input("Entrez la quantité: "))

         transaction = TransactionEntree(code_marchand, nom_produit, quantite_entree)
         try:
            transaction.buy_product()
            rprint("[bold green]Stock mis à jour et transaction enregistrée avec succès![/bold green]")
         except ValueError as e:
            print(f"Erreur: {e}")

      elif choix == "2": # Ajout d'un nouveau stock à un marchand
         code_marchand = input("Entrez l'ID du marchand: ")
         nom_produit = input("Entrez le nom du produit: ")
         quantite_entree = int(input("Entrez la quantité: "))
         prix_unitaire = float(input("Entrez le prix unitaire: "))

         transaction = TransactionEntree(code_marchand, nom_produit, quantite_entree, prix_unitaire)
         try:
            transaction.add_stock()
            rprint("[bold green]Nouveau stock ajouté avec succès![/bold green]")
         except ValueError as e:
            print(f"Erreur: {e}")

      elif choix == "3": # Affichage des transactions d'entrée
         transactions = TransactionEntree.get_all()
            
         if not transactions:
            console.print("[bold red]Aucune transaction trouvée.[/bold red]")
            continue

         table = table_transactionEntre_title()
         for transaction in transactions:
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_entree']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{transaction['montant_total']:.2f}",
               transaction['date_entree']
               )
         console.print(table)

      elif choix == "4": # Affichage des transactions d'entrée d'un marchand
         code_marchand = input("Entrez l'ID du marchand: ")
         transactions = TransactionEntree.get_by_marchand(code_marchand)

         if not transactions:
            console.print(f"[bold red]Aucune transaction trouvée pour le marchand {code_marchand}.[/bold red]")
            continue

         table = table_transactionEntre_title()
         for transaction in transactions:
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_entree']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{transaction['montant_total']:.2f}",
               transaction['date_entree']
            )
         console.print(table)

      elif choix == "5": # Afficher les transactions d'entrée d'un produit
         nom_produit = input("Entrez le nom du produit: ")
         transactions = TransactionEntree.get_by_produit(nom_produit)
         
         if not transactions:
            console.print(f"[bold red]Aucune transaction trouvée pour le produit {nom_produit}.[/bold red]")
            continue
         
         table = table_transactionEntre_title()
         for transaction in transactions:
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_entree']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{transaction['montant_total']:.2f}",
               transaction['date_entree']
            )
         console.print(table)

      elif choix == "6": # Afficher les transactions ayant fait l'objet d'un montant minimum
         montant_min = float(input("Entrez le montant minimum: "))
         transactions = TransactionEntree.get_by_montant_min(montant_min)
         
         if not transactions:
            console.print(f"[bold red]Aucune transaction trouvée avec un montant minimum de {montant_min}.[/bold red]")
            continue
         
         table = table_transactionEntre_title()
         for transaction in transactions:
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_entree']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{transaction['montant_total']:.2f}",
               transaction['date_entree']
            )
         console.print(table)

      elif choix == "7": # Afficher les transactions ayant fait l'objet d'un montant maximum
         montant_max = float(input("Entrez le montant maximum: "))
         transactions = TransactionEntree.get_by_montant_max(montant_max)
         
         if not transactions:
            console.print(f"[bold red]Aucune transaction trouvée avec un montant maximum de {montant_max}.[/bold red]")
            continue
         
         table = table_transactionEntre_title()
         for transaction in transactions:
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_entree']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{transaction['montant_total']:.2f}",
               transaction['date_entree']
            )
         console.print(table)

      elif choix == "8": # Afficher les transactions ayant fait l'objet d'un montant (minimum - maximum)
         montant_min = float(input("Entrez le montant minimum: "))
         montant_max = float(input("Entrez le montant maximum: "))
         transactions = TransactionEntree.get_by_montant_interval(montant_min, montant_max)
         
         if not transactions:
            console.print(f"[bold red]Aucune transaction trouvée entre {montant_min} et {montant_max}.[/bold red]")
            continue
         
         table = table_transactionEntre_title()
         for transaction in transactions:
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_entree']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{transaction['montant_total']:.2f}",
               transaction['date_entree']
            )
         console.print(table)

      elif choix == "9": # Quitter
         console.print("[bold yellow]Merci d'avoir consulté notre service![/bold yellow]", style="bold")
         break
      
      else:
         print("Option invalide, veuillez réessayer.")
