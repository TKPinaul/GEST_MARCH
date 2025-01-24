import random

from configs.bd_connexion import get_database

class Marche:
   """Classe permettant de gérer les marchés"""
   
   def __init__(self, x_ligne=50, y_colonne=50, marche_id=None):
      """ Initialisation d'un marché matriciel de taille x_ligne * y_colonne par defaut 50*50 """
      self.marche_id = marche_id if marche_id else random.randint(1000, 9999) # Générer un id aléatoire si non fourni
      self.x_ligne = x_ligne
      self.y_colonne = y_colonne
      
      self.grille = [[False for _ in range(self.x_ligne)] for _ in range(self.y_colonne)] # False = pas de marchand, True = marchand
      
   def stand_available(self, x, y):
      """ Vérifie si un stand est disponible """
      if (0 <= x < self.x_ligne) and (0 <= y < self.y_colonne):
         return not self.grille[x][y]
      else:
         raise ValueError(f"Les coordonnées (x, y) sont hors de la grille")
   
   def occup_stand(self, x, y):
      """ Occuper un stand """
      if self.stand_available(x, y):
         self.grille[x][y] = True
      else:
         raise ValueError(f"Le stand ({x}, {y}) est déjà occupé ou hors de la grille")
   
   def free_stand(self, x, y):
      """ Libérer un stand """
      if (0 <= x < self.x_ligne) and (0 <= y < self.y_colonne):
         self.grille[x][y] = False
      else:
         raise ValueError(f"Les coordonnées (x, y) sont hors de la grille")
   
   def show_grille(self):
      """ Afficher la grille du marché """
      for stand in self.grille:
         print(stand)
         
   def save(self):
      """Enregistre un marché dans la base de données"""
      db = get_database()
      collection = db['marches'] # Récupérer la collection sinon la créer
      data = {
         'marche_id': self.marche_id,
         'x_ligne': self.x_ligne,
         'y_colonne': self.y_colonne,
         'grille': self.grille
      }
      collection.insert_one(data) # Insérer le marché dans la base de données
   
   @staticmethod
   def get_one(marche_id):
      """Récupère un marché à partir de son marche_id"""
      db = get_database()
      collection = db['marches']
      marche = collection.find_one({'marche_id': marche_id}) # Récupérer le marché
      return marche
   