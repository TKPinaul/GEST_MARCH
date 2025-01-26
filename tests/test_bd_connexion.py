import unittest

from configs.bd_connexion import get_database

class TestDatabaseConnection(unittest.TestCase):
   def test_connection(self):
      """ 
      Teste si la connexion à la base de données est réussie
      """
      try:
         db = get_database() # Récupérer la base de données
         collections = db.list_collection_names() # Récupérer les collections de la base de données
      except Exception as e:
         self.fail(f"La connexion à la base de données a échoué : {e}")
      finally:
         if db is not None:
            db.client.close() # Fermer la connexion à la base de données

if __name__ == "__main__":
   unittest.main() # Exécutez les tests
