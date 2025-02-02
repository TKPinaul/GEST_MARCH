from rich.table import Table

def table_marche_title():
   table = Table(title="Information du marché")
   table.add_column("ID", style="green3", no_wrap=True)
   table.add_column("NOM", style="bright_blue")
   table.add_column("Matrice", style="orange_red1")
   return table

def table_stand_title(nom_marche):
   table = Table(title=f"Liste des stands du marché : {nom_marche}")
   table.add_column("Stand (X, Y)", style="bright_red", no_wrap=True)
   table.add_column("Statut", style="yellow")
   return table

def table_marchand_title():
   table = Table(title="Information sur les marchands")
   table.add_column("ID", style="green3", no_wrap=True)
   table.add_column("NOM", style="bright_blue")
   table.add_column("CONTACT", style="yellow")
   table.add_column("STATUT", style="magenta")
   table.add_column("STAND OCCUPER", style="bright_red")
   table.add_column("MARCHE", style="bright_cyan")
   table.add_column("STOCK", style="orange_red1")
   return table