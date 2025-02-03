from GEST_MARCH.models.marche import Marche
from configs.bd_connexion import get_database
from GEST_MARCH.models.personne import Personne
from pymongo.errors import PyMongoError


class Marchands(Personne):
   """Classe permettant de gérer les marchands"""
   
   def __init__(self, nom, contact, coordonneeX, coordonneeY, type_personne="Marchand", stock=None, code_id=None):
      """Initialisation d'un marchand"""
      super().__init__(nom=nom, contact=contact, type_personne=type_personne, code_id=code_id) # Initialisation de la classe parente
      self.coordonneeX = coordonneeX
      self.coordonneeY = coordonneeY
      self.stock = stock if stock is not None else {} # Stock du marchand (dictionnaire)
      
   def save(self, marche_id):
      """Enregistre un marchand dans la base de données"""
      
      marche_data = Marche.get_one(marche_id)
      if not marche_data:
         raise ValueError(f"Aucun marché trouvé avec l'ID : {marche_id}")
      
      marche = Marche.from_dict(marche_data) # Recréer une instance de Marche
      
      if not marche.stand_available(self.coordonneeX, self.coordonneeY):
        raise ValueError(f"Le stand ({self.coordonneeX}, {self.coordonneeY}) est déjà occupé")

      db = get_database()
      collection = db['marchands'] # Récupérer la collection sinon la créer
      
      data = {
         'code_id': self.code_id,
         'nom': self.nom,
         'contact': self.contact,
         'type_personne': self.type_personne,
         'coordonneeX': self.coordonneeX,
         'coordonneeY': self.coordonneeY,
         'stock': self.stock,
         'marche_id': marche_id
      }
      try:
         collection.insert_one(data) # Insérer le marchand
         if not marche.occup_stand(self.coordonneeX, self.coordonneeY):
            raise ValueError(f"Le stand ({self.coordonneeX}, {self.coordonneeY}) n'a pas pu être occupé")
         marche.update_grille()  # Sauvegarder la grille mise à jour
      except PyMongoError as e:
         raise Exception(f"Erreur de connexion à MongoDB : {e}")
      finally:
         db.client.close()

   def update_stock(self):
      """Mettre a jour le stock d'un marchand"""
      db = get_database()
      collection = db['marchands']
      
      try:
         result = collection.update_one(
            {'code_id': self.code_id},
            {'$set': {'stock': self.stock}}
         )
         return result.modified_count
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la mise à jour du stock : {e}")
      finally:
         db.client.close()

   def update_quantite(self, nom_produit, quantite):
      """Met à jour la quantité d'un produit en stock"""
      if not isinstance(quantite, (int, float)) or quantite < 0:
         raise ValueError("La quantité doit être un nombre positif")
      if nom_produit in self.stock:
         self.stock[nom_produit]['quantite'] = quantite
      else:
         raise ValueError(f"Le produit {nom_produit} n'existe pas dans le stock")
   
   def update_prix(self, nom_produit, prix_unitaire):
      """Met à jour le prix unitaire d'un produit en stock"""
      if not isinstance(prix_unitaire, (int, float)) or prix_unitaire < 0:
         raise ValueError("Le prix unitaire doit être un nombre positif")
      if nom_produit in self.stock:
         self.stock[nom_produit]['prix_unitaire'] = prix_unitaire
      else:
         raise ValueError(f"Le produit {nom_produit} n'existe pas dans le stock")
   
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
      try:
         marche.free_stand(self.coordonneeX, self.coordonneeY) # Libérer le stand
         result = collection.delete_one({'code_id': self.code_id}) # Supprimer le marchand
         return result.deleted_count
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la suppression du marchand : {e}")
      finally:
         db.client.close()
      
      
   @staticmethod
   def get_one(code_id):
      """Récupère un marchand à partir de son code_id"""
      db = get_database()
      collection = db['marchands']
      try:
         marchand = collection.find_one({'code_id': code_id}) # Récupérer le marchand
         return marchand
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la récupération du marchand : {e}")
      finally:
         db.client.close()

   @staticmethod
   def get_all():
      """Récupère tous les marchands"""
      db = get_database()
      try:
         collection = db['marchands']
         marchands = list(collection.find()) # Récupérer tous les marchands
         return marchands
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la récupération des marchands : {e}")
      finally:
         db.client.close()
      
   @staticmethod
   def from_dict(data):
      """Recrée une instance Marchands à partir d'un dictionnaire"""
      return Marchands(
         nom=data['nom'],
         contact=data['contact'],
         coordonneeX=data['coordonneeX'],
         coordonneeY=data['coordonneeY'],
         type_personne=data.get('type_personne', 'Marchand'),
         stock=data.get('stock', {}),
         code_id=data.get('code_id')
      )