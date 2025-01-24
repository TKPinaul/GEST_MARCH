import unittest

from configs.bd_connexion import get_database

class TestDatabaseConnection(unittest.TestCase):
   def test_connection(self):
      """
      Teste si la connexion à la base de données est réussie
      """
      try:
         db = get_database() # Récupérer la base de données

         # Vérifie si la connexion est réussie
         collections = db.list_collection_names()
         print("Collections disponibles :", collections)
         print("Connections réussies")

         # Vérifie si les collections sont une liste
         self.assertIsInstance(collections, list)

      except Exception as e:
         # En cas d'erreur, affichez le message d'erreur
         self.fail(f"La connexion à la base de données a échoué : {e}")
         
      finally:
         # Fermer la connexion
         db.client.close()

if __name__ == "__main__":
   unittest.main()
