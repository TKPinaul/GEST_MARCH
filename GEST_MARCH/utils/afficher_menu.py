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

def transactionSortie_menu():
   print(
   """
   === Gestion des transaction d'entre ===
   0. Afficher la liste des marchands
   1. Vendre un produit
   2. Affichage des transactions de sorties
   3. Affichage des transactions de sorties d'un marchand
   4. Afficher les transactions d'entrée d'un produits
   5. Afficher les transactions ayant fais l'objet d'un montant minimum
   6. Afficher les transactions ayant fais l'objet d'un montant maximum
   7. Afficher les transactions ayant fais l'objet d'un montant (minimum - maximum)
   8. Quitter
   """
   )