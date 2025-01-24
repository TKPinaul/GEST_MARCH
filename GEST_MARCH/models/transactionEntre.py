import datetime
import uuid

from configs.bd_connexion import get_database


class TransactionEntree:
   def __init__(self, code_marchand, nom_produit, quantite_entree, prix_unitaire, transaction_id=None):
      """Initialisation d'une transaction d'entrée"""
      self.transaction_id = transaction_id if transaction_id else str(uuid.uuid4())
      self.code_marchand = code_marchand
      self.nom_produit = nom_produit
      self.quantite_entree = quantite_entree
      self.prix_unitaire = prix_unitaire
      self.montant_total = quantite_entree * prix_unitaire
      self.date_entree = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Date de la transaction
      
      
   def buy_product(self, marchand):
      """Acheter un produit à un marchand"""
      if self.nom_produit in marchand.stock:
         marchand.stock[self.nom_produit]['quantite'] += self.quantite_entree # Ajouter la quantité achetée au stock
      else:
         marchand.stock[self.nom_produit] = {
            'quantite': self.quantite_entree, 
            'prix_unitaire': self.prix_unitaire
         } # Ajouter le produit au stock
      marchand.save()
      
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
      """Récupère toutes les transactions d'entrée"""
      db = get_database()
      collection = db['transactions_entrees']
      transactions = collection.find()
      return transactions
   
   
   @staticmethod
   def get_one(transaction_id):
      """Récupère une transaction d'entrée à partir de son transaction_id"""
      db = get_database()
      collection = db['transactions_entrees']
      transaction = collection.find_one({'transaction_id': transaction_id})
      return transaction
   
   
   @staticmethod
   def get_by_marchand(code_marchand):
      """Récupère toutes les transactions d'entrée d'un marchand"""
      db = get_database()
      collection = db['transactions_entrees']
      transactions = collection.find({'code_marchand': code_marchand})
      return transactions
   
   
   @staticmethod
   def get_by_date(date_entree):
      """Récupère toutes les transactions d'entrée d'une date donnée"""
      db = get_database()
      collection = db['transactions_entrees']
      transactions = collection.find({'date_entree': date_entree})
      return transactions
   
   
   @staticmethod
   def get_by_produit(nom_produit):
      """Récupère toutes les transactions d'entrée d'un produit donné"""
      db = get_database()
      collection = db['transactions_entrees']
      transactions = collection.find({'nom_produit': nom_produit})
      return transactions
   
   
   @staticmethod
   def get_by_montant(montant_total):
      """Récupère toutes les transactions d'entrée d'un montant donné"""
      db = get_database()
      collection = db['transactions_entrees']
      transactions = collection.find({'montant_total': montant_total})
      return transactions
   
   
   @staticmethod
   def get_by_montant_min(montant_min):
      """Récupère toutes les transactions d'entrée d'un montant total supérieur ou égal à montant_min"""
      db = get_database()
      collection = db['transactions_entrees']
      transactions = collection.find({'montant_total': {'$gte': montant_min}})
      return transactions
   
   
   @staticmethod
   def get_by_montant_max(montant_max):
      """Récupère toutes les transactions d'entrée d'un montant total inférieur ou égal à montant_max"""
      db = get_database()
      collection = db['transactions_entrees']
      transactions = collection.find({'montant_total': {'$lte': montant_max}})
      return transactions
   
   
   @staticmethod
   def get_by_montant_interval(montant_min, montant_max):
      """Récupère toutes les transactions d'entrée d'un montant total compris entre montant_min et montant_max"""
      db = get_database()
      collection = db['transactions_entrees']
      transactions = collection.find({'montant_total': {'$gte': montant_min, '$lte': montant_max}})
      return transactions