from rich.table import Table


""" ce fichier contient les entete des tables rich"""

# Affichage des information de marche
def table_marche_title():
   table = Table(title="Information du marché")
   table.add_column("ID", style="green3", no_wrap=True)
   table.add_column("NOM", style="bright_blue")
   table.add_column("Matrice", style="orange_red1")
   return table

# Affichage des stands d'un marche (V1)
def table_stand_title(nom_marche):
   table = Table(title=f"Affichage des stands du marché : {nom_marche}")
   table.add_column("Stand (X, Y)", style="bright_red", no_wrap=True)
   table.add_column("Statut", style="yellow")
   return table

# Affichage des information de marchand
def table_marchand_title():
   table = Table(title="Information sur les marchands")
   table.add_column("ID", style="green3", no_wrap=True)
   table.add_column("NOM", style="bright_blue")
   table.add_column("CONTACT", style="yellow")
   table.add_column("STATUT", style="magenta")
   table.add_column("STAND OCCUPER", style="bright_red")
   table.add_column("MARCHE", style="bright_cyan")
   return table

# Affichage des information du stock d'un marchand
def table_stock_title(nom_marchand):
   table = Table(title=f"affichage des stock de : {nom_marchand}")
   table.add_column("PRODUITS", style="bright_blue")
   table.add_column("QUANTITE EN STOCK", style="yellow")
   table.add_column("PRIX UNITAIRE", style="orange_red1")
   return table

# Affichage des information de transaction (entre en stock)
def table_transactionEntre_title():
   table = Table(title="Transactions d'entrée en stock")
   table.add_column("ID TRANSACTION", style="green3", no_wrap=True)
   table.add_column("ID MARCHAND", style="bright_blue")
   table.add_column("PRODUIT", style="yellow")
   table.add_column("QUANTITÉ", style="magenta")
   table.add_column("PRIX UNITAIRE", style="bright_red")
   table.add_column("MONTANT TOTAL", style="bright_cyan")
   table.add_column("DATE", style="orange_red1")
   return table

# Affichage des information de transaction (sortie de stock)
def table_transactionSortie_title():
   table = Table(title="Transactions de sortie de stock")
   table.add_column("ID TRANSACTION", style="cyan", no_wrap=True)
   table.add_column("ID MARCHAND", style="blue")
   table.add_column("PRODUIT", style="yellow")
   table.add_column("QUANTITÉ", style="green")
   table.add_column("PRIX UNITAIRE", style="bright_magenta")
   table.add_column("MONTANT TOTAL", style="red")
   table.add_column("ID CLIENT", style="blue")
   table.add_column("DATE", style="white")
   return table

# Affichage des information d'utilisateur (personnes)
def table_utilisateur_title():
   table = Table(title="Informations sur les utilisateur")
   table.add_column("ID", style="green3", no_wrap=True)
   table.add_column("NOM", style="bright_blue")
   table.add_column("CONTACT", style="yellow")
   table.add_column("MOTS DE PASSE", style="orange_red1")
   table.add_column("PROFIL", style="bright_red")
   return table

# Affichage de la recherche du panier client
def table_panier_title():
   table = Table(title="Résultats de la recherche")
   table.add_column("ID DU MARCHAND", style="green3", no_wrap=True)
   table.add_column("NOM DU MARCHAND", style="bright_blue")
   table.add_column("STAND", style="yellow")
   table.add_column("PRODUITS", style="orange_red1")
   table.add_column("QUANTITÉ EN STOCK", style="magenta")
   table.add_column("PRIX UNITAIRE", style="bright_red")
   table.add_column("MARCHÉ", style="bright_cyan")
   return table