from decouple import config, UndefinedValueError
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def get_database():
   """Récupère la base de données"""
   
   try:
      # Récupérer les informations de connexion à la base de données à partir de .env
      uri = config('BDURL')
      db_name = config('BDNAME')
   except UndefinedValueError as e: # Si les informations de connexion ne sont pas disponibles
      raise Exception(f"Impossible de récupérer les informations de connexion à la base de données : {e}")
   
   try:
      client = MongoClient(uri) # Connexion à la base de données
      db = client[db_name] # Sélectionnez la base de données
      return db
   except ConnectionFailure as e: # Si la connexion à la base de données échoue
      raise Exception(f"Échec de la connexion à la base de données MongoDB : {e}")
   except Exception as e: # Si une erreur inattendue se produit
     raise Exception(f"Une erreur inattendue s'est produite : {e}")