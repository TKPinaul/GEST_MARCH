from GEST_MARCH.auth.authentification import connexion, inscription
from GEST_MARCH.utils.afficher_menu import section_menu, welcome_menu
from GEST_MARCH.views.gestion_marchand import gestion_marchand
from GEST_MARCH.views.gestion_marche import gestion_marche
from GEST_MARCH.views.gestion_perssonne import gestion_user
from GEST_MARCH.views.gestion_trannsactionSortie import gestion_transaction_sortie
from GEST_MARCH.views.gestion_transactionEntre import gestion_transaction_entree
from rich import print as rprint

def main_test():
   type_personne = None  # Variable pour stocker le type de l'utilisateur connecté
   
   while type_personne is None:
      welcome_menu() # Menu de base
      choix = input("Votre choix: ").strip()
      
      if choix == "0":
         type_personne = "Marchand"
      elif choix == "1":
         type_personne = inscription()
      elif choix == "2":
         type_personne = connexion()
      else:
         rprint("[bold red]Option invalide, veuillez réessayer.[/bold red]")
   
   while True:
      section_menu(type_personne)
      

      choix = input("\nChoisissez une option: ")

      if type_personne == "Admin":
         if choix == "0":
            gestion_user()
         elif choix == "1":
            gestion_marche()
         elif choix == "2":
            gestion_marchand()
         elif choix == "3":
            gestion_transaction_entree()
         elif choix == "4":
            gestion_transaction_sortie()
         elif choix == "5":
            rprint("[bold yellow]Déconnexion en cours...[/bold yellow]\n")
            break
         else:
            rprint("[bold red]Option invalide, veuillez réessayer.[/bold red]")
      
      elif type_personne == "Marchand":
         if choix == "0":
            gestion_marche()
         elif choix == "1":
            gestion_marchand()
         elif choix == "2":
            rprint("[bold yellow]Déconnexion en cours...[/bold yellow]\n")
            break
         else:
            rprint("[bold red]Option invalide, veuillez réessayer.[/bold red]")
      
      elif type_personne == "Client":
         if choix == "0":
            gestion_marche()
         elif choix == "1":
            rprint("[bold yellow]Déconnexion en cours...[/bold yellow]\n")
            break
         else:
            rprint("[bold red]Option invalide, veuillez réessayer.[/bold red]")
      
   

if __name__ == "__main__":
   main_test()