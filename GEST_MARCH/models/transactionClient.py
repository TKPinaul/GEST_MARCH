import datetime
import uuid
from configs.bd_connexion import get_database


class TransactionClient:
   def __init__(self, code_client, code_marchand, nom_produit, quantite_achetee, prix_unitaire, transaction_id=None):
      """Initialisation d'une transaction de sortie"""
      self.transaction_id = transaction_id if transaction_id else str(uuid.uuid4()) # Générer un id aléatoire si non fourni
      self.code_client = code_client
      self.code_marchand = code_marchand
      self.nom_produit = nom_produit
      self.quantite_achetee = quantite_achetee
      self.prix_unitaire = prix_unitaire
      self.montant_total = quantite_achetee * prix_unitaire # Montant total de la transaction
      self.date_sortie = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Date de la transaction
   
   def save_transaction(self):
      """Enregistre une transaction de sortie dans la base de données"""
      db = get_database()
      collection = db['transactions_clients']
      data = {
         'transaction_id': self.transaction_id,
         'code_client': self.code_client,
         'code_marchand': self.code_marchand,
         'nom_produit': self.nom_produit,
         'quantite_achetee': self.quantite_achetee,
         'prix_unitaire': self.prix_unitaire,
         'montant_total': self.montant_total,
         'date_sortie': self.date_sortie
      }
      collection.insert_one(data) # Insérer la transaction de sortie dans la base de données
      
   def achat_produits(self, marchand):
      """Achat de produit à un client"""
      if self.nom_produit in marchand.stock:
         quantite_disponible = marchand.stock[self.nom_produit]['quantite']
         
         if quantite_disponible >= self.quantite_achetee:
            nouvelle_quantite = quantite_disponible - self.quantite_achetee
            marchand.stock[self.nom_produit]['quantite'] = nouvelle_quantite
            
            marchand.update_quantite(self.nom_produit, nouvelle_quantite) # Mettre a jour le stock du marchand
            marchand.update_stock()
            self.save_transaction() # Enregistrer la transction
         else:
            raise ValueError(f"Le stock est insuffisant pour le produits : {self.nom_produit}")
      else:
         raise ValueError(f"Le produit {self.nom_produit} n'existe pas dans le stock du marchand")    


   @staticmethod
   def get_all():
      """Récupère toutes les transactions de sortie"""
      db = get_database()
      collection = db['transactions_clients']
      transactions = list(collection.find()) # Récupérer toutes les transactions de sortie
      return transactions
   
   
   @staticmethod
   def get_one(transaction_id):
      """Récupère une transaction de sortie à partir de son transaction_id"""
      db = get_database()
      collection = db['transactions_clients']
      transaction = collection.find_one({'transaction_id': transaction_id}) # Récupérer la transaction de sortie
      return transaction
   
   @staticmethod
   def get_by_marchand(code_marchand):
      """Récupère toutes les transactions de sortie d'un marchand"""
      db = get_database()
      collection = db['transactions_clients']
      transactions = list(collection.find({'code_marchand': code_marchand})) # Récupérer les transactions de sortie du marchand
      return transactions
   
   @staticmethod
   def get_by_client(code_client):
      """Récupère toutes les transactions d'achat d'un client"""
      db = get_database()
      collection = db['transactions_clients']
      transactions = list(collection.find({'code_client': code_client})) # Récupérer les transactions de sortie d'un client
      return transactions
   
   @staticmethod
   def get_by_date(date_sortie):
      """Récupère toutes les transactions de sortie d'une date donnée"""
      db = get_database()
      collection = db['transactions_clients']
      if isinstance(date_sortie, str):
         date_sortie = datetime.datetime.strptime(date_sortie, "%Y-%m-%d")
      transactions = collection.find({'date_sortie': date_sortie}) # Récupérer les transactions de sortie de la date donnée
      return transactions
   
   @staticmethod
   def get_by_produit(nom_produit):
      """Récupère toutes les transactions de sortie d'un produit donné"""
      db = get_database()
      collection = db['transactions_clients']
      transactions = list(collection.find({'nom_produit': nom_produit})) # Récupérer les transactions de sortie du produit donné
      return transactions
   
   @staticmethod
   def get_by_montant(montant_total):
      """Récupère toutes les transactions de sortie d'un montant total donné"""
      db = get_database()
      collection = db['transactions_clients']
      transactions = list(collection.find({'montant_total': montant_total})) # Récupérer les transactions de sortie du montant total donné
      return transactions
   
   
   @staticmethod
   def get_by_montant_min(montant_min):
      """Récupère toutes les transactions de sortie d'un montant total supérieur ou égal à montant_min"""
      db = get_database()
      collection = db['transactions_clients']
      transactions = list(collection.find({'montant_total': {'$gte': montant_min}})) # Récupérer les transactions de sortie du montant total supérieur ou égal à montant_min
      return transactions
   
   
   @staticmethod
   def get_by_montant_max(montant_max):
      """Récupère toutes les transactions de sortie d'un montant total inférieur ou égal à montant_max"""
      db = get_database()
      collection = db['transactions_clients']
      transactions = list(collection.find({'montant_total': {'$lte': montant_max}})) # Récupérer les transactions de sortie du montant total inférieur ou égal à montant_max
      return transactions
   
   
   @staticmethod
   def get_by_montant_interval(montant_min, montant_max):
      """Récupère toutes les transactions de sortie d'un montant total compris entre montant_min et montant_max"""
      db = get_database()
      collection = db['transactions_clients']
      transactions = list(collection.find({'montant_total': {'$gte': montant_min, '$lte': montant_max}})) # Récupérer les transactions de sortie du montant total compris entre montant_min et montant_max
      return transactions
     