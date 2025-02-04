import uuid
from rich import print as rprint
from rich.console import Console
from GEST_MARCH.models.marchands import Marchands
from GEST_MARCH.models.marche import Marche
from GEST_MARCH.models.personne import Personne
from GEST_MARCH.utils.afficher_menu import users_menu
from GEST_MARCH.utils.afficher_stand import afficher_marche
from GEST_MARCH.utils.fonction_util import controler_type_personne, demander_entier
from GEST_MARCH.utils.table_titre import table_marchand_title, table_marche_title, table_utilisateur_title


def gestion_user():
   console = Console()
   
   while True:
      users_menu()
      choix = input("Choisisser une option: ")
      
      if choix == "0": # Créer un utilisateur
         nom = input("Entreez le nom de l'utilisateur : ")
         contact = input("Entreez le contact de l'utilisateur : ")
         type_personne = controler_type_personne("type de personne (Client, Admin) : ")
         
         mots_passe = None
         if type_personne != "Marchand":
            mots_passe = input("Entrez le mot de passe : ")
         
         try:
            personne = Personne(
               code_id=None,
               nom=nom,
               contact=contact,
               type_personne=type_personne,
               mots_passe=mots_passe
            )
            personne.save(collection_name="personnes")
            rprint(f"[bold green]Utilisateur '{nom}' créé avec succès ![/bold green]")
         except ValueError as e:
            rprint(f"[bold red]Erreur : {e}[/bold red]")
         except Exception as e:
            rprint(f"[bold red]Une erreur s'est produite : {e}[/bold red]")
      
      elif choix == "1": # Créer un marcher
         nom_marche = input("Entrez le nom du marché: ")
         # en absence de coordonne X*Y nous prendrons 50*50
         x_ligne = demander_entier("Entrez le nombre de ligne: ")
         y_colonne = demander_entier("Entrez le nombre de colonne: ")
         marche = Marche(nom_marche, x_ligne, y_colonne)
         marche.save() # Création du marché
         rprint('[green]Marché créé avec succès![/green]')
      
      elif choix == "2": # Créer un marchand
         try:
            marche_id = input("Entrez l'ID du marché où le marchand sera installé: ")
            
            try:
               uuid.UUID(marche_id)
               nom = input("Entrez le nom du marchand: ")
               contact = input("Entrez le contact du marchand: ")
               coordonneeX = demander_entier("Entrez la coordonnée X: ")
               coordonneeY = demander_entier("Entrez la coordonnée Y: ")
            
               stock = {} # initialisation du stock
               while True:
                  response = input("Ajouter du stock ? (O/N): ").strip().upper()
                  if response in ["O", "N"]:
                     break
                  rprint("[yellow]Veuillez entrer uniquement 'O' pour Oui ou 'N' pour Non.[/yellow]")
                  
               while response == "O":
                  produit = input("Entrez le nom du produits: ").strip()
                  quantite = int(input("Quantiter totale a enregistrer: "))
                  prix_unitaire = float(input("Quel est le prix unitaire de ce produits: "))
                  
                  stock[produit] = {
                     'quantite': quantite,
                     'prix_unitaire': prix_unitaire
                  } # Ajout du produitts au stock
                  while True:
                     response = input("Ajouter du stock ? (O/N): ").strip().upper()
                     if response in ["O", "N"]:
                        break
                     rprint("[yellow]Veuillez entrer uniquement 'O' pour Oui ou 'N' pour Non.[/yellow]")
               
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
            
            except ValueError:
               rprint("[red]ID du marché est invalide. Veuillez entrer id valide (consulter option 1!).[/red]")
         
         except ValueError as e:
            console.print(f"[bold red]Erreur: {e}[/bold red]", style="bold")
         except Exception as e:
            console.print(f"[bold red]Erreur inattendue : {e}[/bold red]", style="bold")
      
      elif choix == "3": # Afficher tous les marchés
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
      
      elif choix == "4": # Afficher les stands d'un marché
         marche_id = input("Entrez l'ID du marché: ")
         try:
            uuid.UUID(marche_id)
            
            marche_data = Marche.get_one(marche_id)
            if not marche_data:
               console.print("[bold red]ID du marché incorrect.[/bold red]", style="bold")
               continue
         
            marche = Marche.from_dict(marche_data)
            afficher_marche(marche)
         except ValueError:
            rprint("[red]ID du marché est invalide. Veuillez entrer id valide (consulter option 2!).[/red]")
      
      elif choix == "5": # Affichage de tous les utilisateurs (confondu)
         perssonnes = Personne.get_all()
         
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
      
      elif choix == "6": # Afficher tous les marchands
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
      
      elif choix == "7": # Afficher que les clients
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
         
      elif choix == "8": # Afficher les admins du système
         perssonnes = Personne.get_by_type(type_personne="Admin")
         
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
      
      elif choix == "9":
         console.print("[bold yellow]Merci d'avoir consulté notre service![/bold yellow]", style="bold")
         break
      
      else:
         rprint("[red]Option invalide, Veuillez réessayer[/red]")
            
         