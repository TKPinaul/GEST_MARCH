from decouple import config, UndefinedValueError
from pymongo import MongoClient


def get_database():
   """Récupère la base de données"""
   
   try:
      # Récupérer les informations de connexion à la base de données à partir de .env
      uri = config('BDURL')
      db_name = config('BDNAME')
   except UndefinedValueError as e: 
      # En cas d'erreur, affichez le message d'erreur
      raise Exception(f"Impossible de récupérer les informations de connexion à la base de données : {e}")
   
   client = MongoClient(uri) # Connexion à la base de données   
   db = client[db_name] # Sélectionnez la base de données
   return db
