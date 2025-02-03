from GEST_MARCH.views.gestion_marchand import gestion_marchand
from GEST_MARCH.views.gestion_marche import gestion_marche
from GEST_MARCH.views.gestion_trannsactionSortie import gestion_transaction_sortie
from GEST_MARCH.views.gestion_transactionEntre import gestion_transaction_entree
from rich import print as rprint

def main():
   while True:
      rprint("\n=== Menu Principal ===")
      print("1. Gestion des Marchés")
      print("2. Gestion des Marchands")
      print("3. Gestion des Transactions d'Entrée (rentre de stock)")
      print("4. Gestion des Transactions de Sortie (sorties de stock)")
      print("5. Quitter")

      choix = input("\nChoisissez une option: ")

      if choix == "1":
         gestion_marche()
      elif choix == "2":
         gestion_marchand()
      elif choix == "3":
         gestion_transaction_entree()
      elif choix == "4":
         gestion_transaction_sortie()
      elif choix == "5":
         rprint("[bold yellow]Au revoir et à bientôt![/bold yellow]\n")
         break
      else:
         rprint("[bold red]Option invalide, veuillez réessayer.[/bold red]")


if __name__ == "__main__":
   main()