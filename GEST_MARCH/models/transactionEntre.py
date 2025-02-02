import datetime
import uuid
from GEST_MARCH.models.marchands import Marchands
from configs.bd_connexion import get_database


class TransactionEntree:
   def __init__(self, code_marchand, nom_produit, quantite_entree, prix_unitaire=None, transaction_id=None):
      """Initialisation d'une transaction d'entrée"""
      self.transaction_id = transaction_id if transaction_id else str(uuid.uuid4())
      self.code_marchand = code_marchand
      self.nom_produit = nom_produit
      self.quantite_entree = quantite_entree
      self.prix_unitaire = prix_unitaire
      self.montant_total = None
      self.date_entree = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

   def buy_product(self):
      """Augmenter les stocks d'un marchand et enregistrer la transaction"""
      marchand_data = Marchands.get_one(self.code_marchand)
      if not marchand_data:
         raise ValueError(f"Aucun marchand trouvé avec le code ID : {self.code_marchand}")
        
      marchand = Marchands.from_dict(marchand_data)
        
      if self.nom_produit in marchand.stock:
         prix_unitaire_exist = marchand.stock[self.nom_produit].get('prix_unitaire')
         if prix_unitaire_exist:
            self.prix_unitaire = prix_unitaire_exist
         else:
            raise ValueError(f"Le produit '{self.nom_produit}' n'a pas de prix unitaire défini.")
         marchand.stock[self.nom_produit]['quantite'] += self.quantite_entree # Augmenter la quantité en stock
      else:
         marchand.stock[self.nom_produit] = {
            'quantite': self.quantite_entree,
            'prix_unitaire': self.prix_unitaire
         }
        
      marchand.update_stock()
      self.montant_total = self.quantite_entree * self.prix_unitaire
      self.save_transaction()

   def add_stock(self):
      """Ajoute du stock à un marchand par son ID"""
      marchand_data = Marchands.get_one(self.code_marchand)
      if not marchand_data:
         raise ValueError(f"Aucun marchand trouvé avec le code ID : {self.code_marchand}")
        
      marchand = Marchands.from_dict(marchand_data)
        
      if self.nom_produit in marchand.stock:
         marchand.stock[self.nom_produit]['quantite'] += self.quantite_entree
      else:
         marchand.stock[self.nom_produit] = {
            'quantite': self.quantite_entree,
            'prix_unitaire': self.prix_unitaire
         }
        
      marchand.update_stock()
      self.montant_total = self.quantite_entree * self.prix_unitaire
      self.save_transaction()

   def save_transaction(self):
      """Enregistre une transaction d'entrée dans la base de données"""
      db = get_database()
      collection = db['transactions_entrees']
      data = {
         'transaction_id': self.transaction_id,
         'code_marchand': self.code_marchand,
         'nom_produit': self.nom_produit,
         'quantite_entree': self.quantite_entree,
         'prix_unitaire': self.prix_unitaire,
         'montant_total': self.montant_total,
         'date_entree': self.date_entree
      }
      collection.insert_one(data)

   @staticmethod
   def get_all():
      db = get_database()
      collection = db['transactions_entrees']
      return list(collection.find())

   @staticmethod
   def get_one(transaction_id):
      db = get_database()
      collection = db['transactions_entrees']
      return collection.find_one({'transaction_id': transaction_id})

   @staticmethod
   def get_by_marchand(code_marchand):
      db = get_database()
      collection = db['transactions_entrees']
      return list(collection.find({'code_marchand': code_marchand}))
   
   @staticmethod
   def get_by_produit(nom_produit):
      db = get_database()
      collection = db['transactions_entrees']
      return list(collection.find({'nom_produit': nom_produit}))
   
   @staticmethod
   def get_by_montant_min(montant_min):
      db = get_database()
      collection = db['transactions_entrees']
      return list(collection.find({'montant_total': {'$gte': montant_min}}))
   
   @staticmethod
   def get_by_montant_max(montant_max):
      db = get_database()
      collection = db['transactions_entrees']
      return list(collection.find({'montant_total': {'$lte': montant_max}}))
   
   @staticmethod
   def get_by_montant_interval(montant_min, montant_max):
      db = get_database()
      collection = db['transactions_entrees']
      return list(collection.find({'montant_total': {'$gte': montant_min, '$lte': montant_max}}))


