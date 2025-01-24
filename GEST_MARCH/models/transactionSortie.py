import datetime
import uuid

from configs.bd_connexion import get_database


class TransactionSortie:
   def __init__(self, code_marchand, nom_produit, quantite_vendue, prix_unitaire, transaction_id=None):
      """Initialisation d'une transaction de sortie"""
      self.transaction_id = transaction_id if transaction_id else str(uuid.uuid4()) # Générer un id aléatoire si non fourni
      self.code_marchand = code_marchand
      self.nom_produit = nom_produit
      self.quantite_vendue = quantite_vendue
      self.prix_unitaire = prix_unitaire
      self.montant_total = quantite_vendue * prix_unitaire # Montant total de la transaction
      self.date_sortie = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Date de la transaction
   
   
   def sell_product(self, marchand):
      """Vend un produit à un client"""
      if self.nom_produit in marchand.stock:
         if marchand.stock[self.nom_produit]['quantite'] >= self.quantite_vendue:
            marchand.stock[self.nom_produit]['quantite'] -= self.quantite_vendue # retirer la quantité vendue du stock
            marchand.save() # Enregistrer les modifications
            self.save_transaction()
         else:
            raise ValueError(f"Le stock est insuffisnat pour le produits : {self.nom_produit}")
      else:
         raise ValueError(f"Le produit {self.nom_produit} n'existe pas dans le stock du marchand")
     
      
   def save_transaction(self):
      """Enregistre une transaction de sortie dans la base de données"""
      db = get_database()
      collection = db['transactions_sorties']
      data = {
         'transaction_id': self.transaction_id,
         'code_marchand': self.code_marchand,
         'nom_produit': self.nom_produit,
         'quantite_vendue': self.quantite_vendue,
         'prix_unitaire': self.prix_unitaire,
         'montant_total': self.montant_total,
         'date_sortie': self.date_sortie
      }
      collection.insert_one(data) # Insérer la transaction de sortie dans la base de données
      
      
   @staticmethod
   def get_all():
      """Récupère toutes les transactions de sortie"""
      db = get_database()
      collection = db['transactions_sorties']
      transactions = collection.find() # Récupérer toutes les transactions de sortie
      return transactions
   
   
   @staticmethod
   def get_one(transaction_id):
      """Récupère une transaction de sortie à partir de son transaction_id"""
      db = get_database()
      collection = db['transactions_sorties']
      transaction = collection.find_one({'transaction_id': transaction_id}) # Récupérer la transaction de sortie
      return transaction
   
   
   @staticmethod
   def get_by_marchand(code_marchand):
      """Récupère toutes les transactions de sortie d'un marchand"""
      db = get_database()
      collection = db['transactions_sorties']
      transactions = collection.find({'code_marchand': code_marchand}) # Récupérer les transactions de sortie du marchand
      return transactions
   
   
   @staticmethod
   def get_by_date(date_sortie):
      """Récupère toutes les transactions de sortie d'une date donnée"""
      db = get_database()
      collection = db['transactions_sorties']
      transactions = collection.find({'date_sortie': date_sortie}) # Récupérer les transactions de sortie de la date donnée
      return transactions
   
   
   @staticmethod
   def get_by_produit(nom_produit):
      """Récupère toutes les transactions de sortie d'un produit donné"""
      db = get_database()
      collection = db['transactions_sorties']
      transactions = collection.find({'nom_produit': nom_produit}) # Récupérer les transactions de sortie du produit donné
      return transactions
   
   
   @staticmethod
   def get_by_montant(montant_total):
      """Récupère toutes les transactions de sortie d'un montant total donné"""
      db = get_database()
      collection = db['transactions_sorties']
      transactions = collection.find({'montant_total': montant_total}) # Récupérer les transactions de sortie du montant total donné
      return transactions
   
   
   @staticmethod
   def get_by_montant_min(montant_min):
      """Récupère toutes les transactions de sortie d'un montant total supérieur ou égal à montant_min"""
      db = get_database()
      collection = db['transactions_sorties']
      transactions = collection.find({'montant_total': {'$gte': montant_min}}) # Récupérer les transactions de sortie du montant total supérieur ou égal à montant_min
      return transactions
   
   
   @staticmethod
   def get_by_montant_max(montant_max):
      """Récupère toutes les transactions de sortie d'un montant total inférieur ou égal à montant_max"""
      db = get_database()
      collection = db['transactions_sorties']
      transactions = collection.find({'montant_total': {'$lte': montant_max}}) # Récupérer les transactions de sortie du montant total inférieur ou égal à montant_max
      return transactions
   
   
   @staticmethod
   def get_by_montant_interval(montant_min, montant_max):
      """Récupère toutes les transactions de sortie d'un montant total compris entre montant_min et montant_max"""
      db = get_database()
      collection = db['transactions_sorties']
      transactions = collection.find({'montant_total': {'$gte': montant_min, '$lte': montant_max}}) # Récupérer les transactions de sortie du montant total compris entre montant_min et montant_max
      return transactions
     