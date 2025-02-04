from rich import print as rprint
from rich.console import Console
from GEST_MARCH.models.personne import Personne

console = Console()

def inscription():
   """Inscription d'une personne"""
   type_personne = "Client"
   
   nom = input("Entreez votre nom et prenom : ").strip()
   contact = input("Entreez votre contact : ").strip()
   
   while True:
      mots_passe = input("Entrez le mot de passe : ").strip()
      confirmation = input("Confirmez le mot de passe : ").strip()
      
      if mots_passe == confirmation:
         break
      else:
         rprint("[bold red]Les mots de passe ne correspondent pas. Réessayez.[/bold red]")
         
   try:
      personne = Personne(
         code_id=None,
         nom=nom,
         contact=contact,
         type_personne=type_personne,
         mots_passe=mots_passe
      )
      personne.save(collection_name="personnes")
      rprint(f"[bold green]M./Mm '{nom}', votre compte a été créé avec succès ![/bold green]")
      return type_personne
   except ValueError as e:
      rprint(f"[bold red]Erreur : {e}[/bold red]")
   except Exception as e:
      rprint(f"[bold red]Une erreur s'est produite : {e}[/bold red]")
      
      
def connexion():
   """Phase de connexion"""
   essais_restants = 3
   nom = input("Entreez votre nom de compte : ").strip()
   
   try:
      personne_data = Personne.get_by_nom("personnes", nom)
      
      if not personne_data: # vérifier si la perssonne existe
         rprint(f"[bold red]Aucun compte trouvé pour {nom} veuillez réesayer avec un nom valide[/bold red]")
         return None
      
      personne_data = personne_data[0]
      personne = Personne.from_dict(personne_data)
      
      while essais_restants > 0:
         mots_passe = input("Entrez le mot de passe : ").strip()
         
         if personne.verifier_pass(mots_passe):
            rprint(f"[bold green]Bienvenue {nom}, connexion réussie ![/bold green]")
            return personne.type_personne  # Retourne le type de compte après connexion
         
         essais_restants -= 1
         if essais_restants > 0:
            rprint(f"[bold yellow]Mot de passe incorrect. Il vous reste {essais_restants} essai(s).[/bold yellow]")
         else:
            rprint("[bold red]Identification rejetée ![/bold red]")
            
   except Exception as e:
      rprint(f"[bold red]Une erreur s'est produite : {e}[/bold red]")
   return None