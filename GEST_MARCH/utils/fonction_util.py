from rich import print as rprint

def demander_entier(message):
   while True:
      try:
         valeur = int(input(message))
         if valeur > 0:
            return valeur
         else:
            rprint("[bold yellow]Veuillez entrer un nombre entier strictement positif ![/bold yellow]")
      except ValueError:
         rprint("[bold yellow]Veuillez entrer un nombre entier valide (ex: 1, 2, 3...) ![/bold yellow]")
