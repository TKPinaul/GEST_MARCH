from decouple import config
from pymongo import MongoClient


def get_database():
   # Récupérer les informations de connexion à la base de données à partir de .env
   uri = config('BDURL')
   db_name = config('BDNAME')

   # Connexion à la base de données
   client = MongoClient(uri)

   # Sélectionnez la base de données
   db = client[db_name]
   return db
