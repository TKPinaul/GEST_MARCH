from rich import print as rprint

def welcome_menu():
   rprint(
   """
   === Bienvenue ! Que puis-je faire pour vous ? ===
   
   0. Je suis un marchand
   1. Je souhaite m'enregistrer en tant que client
   2. J'ai un compte et je veux me connecter
   """
   )
   
def section_menu(type_personne):
   """Affiche le menu en fonction du type d'utilisateur."""
   print(f"""
      === Menu Principal ({type_personne})===""")
   
   if type_personne == "Admin":
      print(
      """
      0. Gestion des Utilisateurs
      1. Accéder aux Marchés
      2. Accéder aux fonctionnalités Marchand
      3. Gestion des Transactions d'Entrée (rentrée de stock)
      4. Gestion des Transactions de Sortie (sortie de stock)
      5. Quitter""")
   
   elif type_personne == "Marchand":
      print("""
      0. Accéder aux Marchés
      1. Accéder aux fonctionnalités Marchand
      2. Quitter """)
   
   elif type_personne == "Client":
      print("""
      0. Accéder aux Marchés
      1. Consulter le catalogue
      2. Quitter """)
   

def users_menu():
   print(
      """
      === Gestion des utilisateurs ===
      0. Créer un utilisateur
      1. Créer un marché
      2. Créer un marchand
      3. Afficher tous les marchés
      4. Afficher les stands d'un marché
      5. Afficher tous les utilisateurs
      6. Afficher tous les marchands
      7. Afficher tous les clients
      8. Afficher les admin du système
      9. Quitter
      """
   )

def marche_menu():
   print(
      """
      === Gestions des Marchés ===
      0. Afficher tous les marchés
      1. Afficher un marché
      2. Afficher les stands d'un marché
      3. Quitter
      """
   )
   
def marchand_menu():
   print(
      """
      === Gestions des Marchands ===
      0. Afficher les marchés
      1. Afficher les stand d'un marché
      2. Afficher tous les marchands
      3. Afficher les information d'un marchand
      4. Afficher les stocks d'un marchand
      5. Modifier un marchand
      6. Supprimer un marchand
      7. Quitter
      """
   )

def transactionEntre_menu():
   print(
   """
   === Gestion des transaction d'entre ===
   0. Afficher la liste des marchands
   1. Ravitaillement de stock d'un marchand
   2. Ajoutet un nouveau stock à un marchand
   3. Affichage des transactions d'entrée
   4. Affichage des transaction d'entrée d'un marchand
   5. Afficher les transaction d'entrée d'un produits
   6. Afficher les transactions ayant fais l'objet d'un montant minimum
   7. Afficher les transactions ayant fais l'objet d'un montant maximum
   8. Afficher les transactions ayant fais l'objet d'un montant (minimum - maximum)
   9. Quitter
   """
   )

def client_menu():
   print(
   """
   === Gestion des transaction d'entre ===
   0. Afficher la liste des marchands
   1. Afficher les produits d'un marchants
   2. Rechercher une liste de produit
   3. Acheter un produit
   4. Quitter
   """
   )
   
def transactionSortie_menu():
   print(
   """
   === Gestion des transaction d'entre ===
   0. Afficher la liste des marchands
   1. Afficher des transactions de sorties
   2. Afficher les transaction d'un client
   3. Afficher des transactions de sorties d'un marchand
   4. Afficher les transactions d'entrée d'un produits
   5. Afficher les transactions ayant fais l'objet d'un montant minimum
   6. Afficher les transactions ayant fais l'objet d'un montant maximum
   7. Afficher les transactions ayant fais l'objet d'un montant (minimum - maximum)
   8. Quitter
   """
   )