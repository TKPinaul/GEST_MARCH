from GEST_MARCH.models.personne import Personne
from configs.bd_connexion import get_database


class Marchands(Personne):
   """Classe permettant de gérer les marchands"""
   
   def __init__(self, nom, contact, coordonneeX, coordonneeY, type_personne="Marchand", stock=None, code_id=None):
      """Initialisation d'un marchand"""
      super().__init__(nom, contact, type_personne, code_id) # Initialisation de la classe parente
      self.coordonneeX = coordonneeX
      self.coordonneeY = coordonneeY
      self.stock = stock if stock is not None else {} # Stock du marchand (dictionnaire)
      
      
   def save(self):
      """Enregistre un marchand dans la base de données"""
      db = get_database()
      collection = db['marchands'] # Récupérer la collection sinon la créer
      data = {
         'code_id': self.code_id,
         'nom': self.nom,
         'contact': self.contact,
         'type_personne': self.type_personne,
         'coordonneeX': self.coordonneeX,
         'coordonneeY': self.coordonneeY,
         'stock': self.stock
      }
      collection.insert_one(data) # Insérer le marchand


   def update_quantite(self, nom_produit, quantite):
      """Met à jour la quantité d'un produit en stock"""
      if nom_produit in self.stock:
         self.stock[nom_produit]['quantite'] = quantite
      else:
         raise ValueError(f"Le produit {nom_produit} n'existe pas dans le stock")
   
   
   def update_prix(self, nom_produit, prix_unitaire):
      """Met à jour le prix unitaire d'un produit en stock"""
      if nom_produit in self.stock:
         self.stock[nom_produit]['prix_unitaire'] = prix_unitaire
      else:
         raise ValueError(f"Le produit {nom_produit} n'existe pas dans le stock")
   
   
   def occup_stand(self, marche):
      """Occuper un stand dans un marché avec marche : Instance de la classe Marche"""
      if marche.stand_available(self.coordonneeX, self.coordonneeY):
         marche.occup_stand(self.coordonneeX, self.coordonneeY) # Occuper le stand
      else:
         raise ValueError(f"Le stand ({self.coordonneeX}, {self.coordonneeY}) est déjà occupé ou hors de la grille")
   
   
   def change_stand(self, marche, new_x, new_y):
      """Changer de stand dans un marché"""
      if marche.stand_available(new_x, new_y):
         marche.free_stand(self.coordonneeX, self.coordonneeY) # Libérer l'ancien stand
         self.coordonneeX = new_x
         self.coordonneeY = new_y
         marche.occup_stand(new_x, new_y)
      else:
         raise ValueError(f"Le stand ({new_x}, {new_y}) est déjà occupé ou hors de la grille")
      
      
   def delete_marchand(self, marche):
      """Supprime un marchand et libère son stand"""
      db = get_database()
      collection = db['marchands']
      marche.delete_stand(self.coordonneeX, self.coordonneeY) # Libérer le stand
      result = collection.delete_one({'code_id': self.code_id}) # Supprimer le marchand
      return result.deleted_count
      
      
   @staticmethod
   def get_one(code_id):
      """Récupère un marchand à partir de son code_id"""
      db = get_database()
      collection = db['marchands']
      marchand = collection.find_one({'code_id': code_id}) # Récupérer le marchand
      return marchand
   
   @staticmethod
   def get_all():
      """Récupère tous les marchands"""
      db = get_database()
      collection = db['marchands']
      marchands = collection.find() # Récupérer tous les marchands
      return marchands