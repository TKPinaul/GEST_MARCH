from rich import print as rprint

def demander_entier(message):
   while True:
      try:
         valeur = int(input(message).strip())
         if valeur >= 0:
            return valeur
         else:
            rprint("[bold yellow]Veuillez entrer un nombre entier strictement positif ![/bold yellow]")
      except ValueError:
         rprint("[bold yellow]Veuillez entrer un nombre entier valide (ex: 1, 2, 3...) ![/bold yellow]")
         
def demander_reel(message):
   while True:
      try:
         valeur = float(input(message).strip())
         if valeur >= 0:
            return valeur
         else:
            rprint("[bold yellow]Veuillez entrer un nombre entier strictement positif ![/bold yellow]")
      except ValueError:
         rprint("[bold yellow]Veuillez entrer un nombre entier valide (ex: 1, 2, 3...) ![/bold yellow]")

def controler_type_personne(message):
   TYPES_PERSSONNES = ["Client", "Admin"]
   
   while True:
      type_personne = input(message).strip().capitalize()
      if type_personne in TYPES_PERSSONNES:
         return type_personne
      else:
         rprint(f"[bold red]Type de personne invalide. Veuillez choisir parmi : {', '.join(TYPES_PERSSONNES)}.[/bold red]")
         