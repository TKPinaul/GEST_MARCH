import uuid
from rich import print as rprint
from rich.console import Console

from GEST_MARCH.models.marchands import Marchands
from GEST_MARCH.models.marche import Marche
from GEST_MARCH.models.personne import Personne
from GEST_MARCH.models.transactionClient import TransactionClient
from GEST_MARCH.utils.afficher_menu import transactionSortie_menu
from GEST_MARCH.utils.fonction_util import demander_reel
from GEST_MARCH.utils.table_titre import table_marchand_title, table_transactionSortie_title, table_utilisateur_title


def gestion_transaction_sortie():
   console = Console()
   
   while True:
      transactionSortie_menu()
      choix = input("Choisissez une option: ")

      if choix == "0": # Afficher la liste des marchands
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
      
      if choix == "1": # Afficher la liste des clients
         perssonnes = Personne.get_by_type(type_personne="Client")
         
         if not perssonnes: # Vérifier l'existance de personne/utilisateur dans la BD
            rprint("[bold red]Aucun utilisateur trouvé.[/bold red]")
            continue
         
         table = table_utilisateur_title()
         for perssonne_data in perssonnes:
            perssonne = Personne.from_dict(perssonne_data)
            table.add_row(
               perssonne.code_id,
               perssonne.nom,
               perssonne.contact,
               "*************" if perssonne.get_mots_passe() else "N/A",
               perssonne.type_personne
            ) 
         console.print(table)

      elif choix == "2": # Affichage des transactions de sortie
         transactions = TransactionClient.get_all()
         
         if not transactions:
            console.print("[bold red]Aucune transaction trouvée.[/bold red]")
            continue
         
         table = table_transactionSortie_title()
         for transaction in transactions:
            montant_total = transaction['montant_total']
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_achetee']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{montant_total:.2f}" if montant_total is not None else "[blod red3]N/A[/blod red3]",
               transaction['code_client'],
               transaction['date_sortie']
               )
         console.print(table)

      if choix == "3": # Afficher les transaction d'un client
         code_client = input("Entrez l'ID du client: ").strip()
         try:
            uuid.UUID(code_client)
            transactions = TransactionClient.get_by_client(code_client)

            if not transactions:
               console.print(f"[bold red]Aucune transaction trouvée pour le marchand {code_marchand}.[/bold red]")
               continue
            
            table = table_transactionSortie_title()
            for transaction in transactions:
               montant_total = transaction['montant_total']
               table.add_row(
                  transaction['transaction_id'],
                  transaction['code_marchand'],
                  transaction['nom_produit'],
                  str(transaction['quantite_achetee']),
                  f"{transaction['prix_unitaire']:.2f}",
                  f"{montant_total:.2f}" if montant_total is not None else "[blod red3]N/A[/blod red3]",
                  transaction['code_client'],
                  transaction['date_sortie']
                  )
            console.print(table)
         except ValueError:
            rprint("[red]ID du client est invalide. Veuillez entrer id valide (consulter option 1!).[/red]")
            
      elif choix == "4": # Affichage des transactions de sortie d'un marchand
         code_marchand = input("Entrez l'ID du marchand: ").strip()
         try:
            uuid.UUID(code_marchand)
            transactions = TransactionClient.get_by_marchand(code_marchand)

            if not transactions:
               console.print(f"[bold red]Aucune transaction trouvée pour le marchand {code_marchand}.[/bold red]")
               continue
            
            table = table_transactionSortie_title()
            for transaction in transactions:
               montant_total = transaction['montant_total']
               table.add_row(
                  transaction['transaction_id'],
                  transaction['code_marchand'],
                  transaction['nom_produit'],
                  str(transaction['quantite_achetee']),
                  f"{transaction['prix_unitaire']:.2f}",
                  f"{montant_total:.2f}" if montant_total is not None else "[blod red3]N/A[/blod red3]",
                  transaction['code_client'],
                  transaction['date_sortie']
                  )
            console.print(table)
         except ValueError:
            rprint("[red]ID du client est invalide. Veuillez entrer id valide (consulter option 0!).[/red]")

      elif choix == "5": # Afficher les transactions de sortie d'un produit
         nom_produit = input("Entrez le nom du produit: ").strip()
         transactions = TransactionClient.get_by_produit(nom_produit)
         
         if not transactions:
            console.print(f"[bold red]Aucune transaction trouvée pour le produit {nom_produit}.[/bold red]")
            continue
         
         table = table_transactionSortie_title()
         for transaction in transactions:
            montant_total = transaction['montant_total']
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_achetee']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{montant_total:.2f}" if montant_total is not None else "[blod red3]N/A[/blod red3]",
               transaction['code_client'],
               transaction['date_sortie']
               )
         console.print(table)

      elif choix == "6": # Afficher les transactions ayant fais l'objet d'un montant minimum
         montant_min = demander_reel("Entrez le montant minimum: ")
         transactions = TransactionClient.get_by_montant_min(montant_min)
         
         if not transactions:
            console.print(f"[bold red]Aucune transaction trouvée avec un montant minimum de {montant_min}.[/bold red]")
            continue
         
         table = table_transactionSortie_title()
         for transaction in transactions:
            montant_total = transaction['montant_total']
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_achetee']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{montant_total:.2f}" if montant_total is not None else "[blod red3]N/A[/blod red3]",
               transaction['code_client'],
               transaction['date_sortie']
               )
         console.print(table)

      elif choix == "7": # Afficher les transactions ayant fais l'objet d'un montant maximum
         montant_max = demander_reel("Entrez le montant maximum: ")
         transactions = TransactionClient.get_by_montant_max(montant_max)
         
         if not transactions:
            console.print(f"[bold red]Aucune transaction trouvée avec un montant maximum de {montant_max}.[/bold red]")
            continue
         
         table = table_transactionSortie_title()
         for transaction in transactions:
            montant_total = transaction['montant_total']
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_achetee']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{montant_total:.2f}" if montant_total is not None else "[blod red3]N/A[/blod red3]",
               transaction['date_sortie']
               )
         console.print(table)

      elif choix == "8": # Afficher les transactions ayant fais l'objet d'un montant (minimum - maximum)
         montant_min = demander_reel("Entrez le montant minimum: ")
         montant_max = demander_reel("Entrez le montant maximum: ")
         transactions = TransactionClient.get_by_montant_interval(montant_min, montant_max)
         
         if not transactions:
            console.print(f"[bold red]Aucune transaction trouvée entre {montant_min} et {montant_max}.[/bold red]")
            continue
         
         table = table_transactionSortie_title()
         for transaction in transactions:
            montant_total = transaction['montant_total']
            table.add_row(
               transaction['transaction_id'],
               transaction['code_marchand'],
               transaction['nom_produit'],
               str(transaction['quantite_achetee']),
               f"{transaction['prix_unitaire']:.2f}",
               f"{montant_total:.2f}" if montant_total is not None else "[blod red3]N/A[/blod red3]",
               transaction['date_sortie']
               )
         console.print(table)

      elif choix == "9": # Quitter
         console.print("[bold yellow]Merci d'avoir consulté notre service![/bold yellow]", style="bold")
         break
      
      else:
         print("Option invalide, veuillez réessayer.")