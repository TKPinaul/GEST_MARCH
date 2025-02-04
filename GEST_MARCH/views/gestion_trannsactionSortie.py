from GEST_MARCH.models.marchands import Marchands
from GEST_MARCH.models.transactionClient import TransactionClient
from GEST_MARCH.utils.afficher_menu import transactionSortie_menu


def gestion_transaction_sortie():
    while True:
      transactionSortie_menu()
      choix = input("Choisissez une option: ")

      if choix == "1":
         # Vendre produit
         code_marchand = input("Entrez l'ID du marchand: ")
         nom_produit = input("Entrez le nom du produit: ")
         quantite_vendue = int(input("Entrez la quantité vendue: "))
         prix_unitaire = float(input("Entrez le prix unitaire: "))
         transaction = TransactionClient(code_marchand, nom_produit, quantite_vendue, prix_unitaire)
         transaction.sell_product(Marchands.get_one(code_marchand))
         print("Transaction de sortie enregistrée avec succès!")

      elif choix == "2":
         # Affichage des transactions de sortie
         transactions = TransactionClient.get_all()
         for transaction in transactions:
            print(f"ID: {transaction['transaction_id']}, Marchand: {transaction['code_marchand']}, Produit: {transaction['nom_produit']}, Quantité: {transaction['quantite_vendue']}, Montant: {transaction['montant_total']}")

      elif choix == "3":
         # Affichage des transactions de sortie d'un marchand
         code_marchand = input("Entrez l'ID du marchand: ")
         transactions = TransactionClient.get_by_marchand(code_marchand)
         for transaction in transactions:
            print(f"ID: {transaction['transaction_id']}, Produit: {transaction['nom_produit']}, Quantité: {transaction['quantite_vendue']}, Montant: {transaction['montant_total']}")

      elif choix == "4":
         # Afficher les transactions de sortie d'un produit
         nom_produit = input("Entrez le nom du produit: ")
         transactions = TransactionClient.get_by_produit(nom_produit)
         for transaction in transactions:
            print(f"ID: {transaction['transaction_id']}, Marchand: {transaction['code_marchand']}, Quantité: {transaction['quantite_vendue']}, Montant: {transaction['montant_total']}")

      elif choix == "5":
         # Afficher les transactions ayant fait l'objet d'un montant minimum
         montant_min = float(input("Entrez le montant minimum: "))
         transactions = TransactionClient.get_by_montant_min(montant_min)
         for transaction in transactions:
            print(f"ID: {transaction['transaction_id']}, Marchand: {transaction['code_marchand']}, Produit: {transaction['nom_produit']}, Montant: {transaction['montant_total']}")

      elif choix == "6":
         # Afficher les transactions ayant fait l'objet d'un montant maximum
         montant_max = float(input("Entrez le montant maximum: "))
         transactions = TransactionClient.get_by_montant_max(montant_max)
         for transaction in transactions:
            print(f"ID: {transaction['transaction_id']}, Marchand: {transaction['code_marchand']}, Produit: {transaction['nom_produit']}, Montant: {transaction['montant_total']}")

      elif choix == "7":
         # Afficher les transactions ayant fait l'objet d'un montant (minimum - maximum)
         montant_min = float(input("Entrez le montant minimum: "))
         montant_max = float(input("Entrez le montant maximum: "))
         transactions = TransactionClient.get_by_montant_interval(montant_min, montant_max)
         for transaction in transactions:
            print(f"ID: {transaction['transaction_id']}, Marchand: {transaction['code_marchand']}, Produit: {transaction['nom_produit']}, Montant: {transaction['montant_total']}")

      elif choix == "8":
         break
      else:
         print("Option invalide, veuillez réessayer.")