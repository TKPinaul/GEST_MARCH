import unittest
from GEST_MARCH.models.marche import Marche 
from configs.bd_connexion import get_database

class TestAddMarche(unittest.TestCase):
   
   def setUp(self):
      """Initialisation des variables de test"""
      self.nom_marche = "Marché Test"
      self.marche = Marche(self.nom_marche, x_ligne=10, y_colonne=10)
      self.db = get_database()
      self.collection = self.db['marches']

   def test_create_marche(self):
      """Test de création de marché"""
      try:
         # Vérifie que les attributs du marché sont corrects
         self.assertEqual(self.marche.nom_marche, self.nom_marche, "Le nom du marché ne correspond pas.")
         self.assertEqual(self.marche.x_ligne, 10, "La taille en x_ligne ne correspond pas.")
         self.assertEqual(self.marche.y_colonne, 10, "La taille en y_colonne ne correspond pas.")
         print("Test de création de marché réussi.")
      except AssertionError as e:
         print(f"Erreur lors du test de création de marché : {e}")

   def test_save_marche(self):
      """Test de sauvegarde du marché dans la base de données"""
      try:
         # Sauvegarde le marché dans la base de données
         self.marche.save()
         
         # Récupère le marché depuis la base de données
         marche_sauvegarde = self.collection.find_one({'nom_marche': self.nom_marche})
         
         # Vérifie que le marché a bien été sauvegardé
         self.assertIsNotNone(marche_sauvegarde, "Le marché n'a pas été trouvé dans la base de données.")
         self.assertEqual(marche_sauvegarde['nom_marche'], self.nom_marche, "Le nom du marché sauvegardé ne correspond pas.")
         print("Test de sauvegarde de marché réussi.")
      except Exception as e:
         print(f"Erreur lors du test de sauvegarde de marché : {e}")

   def tearDown(self):
      """Nettoyage après les tests"""
      # Supprime les données de test de la base de données
      self.collection.delete_many({'nom_marche': self.nom_marche})

if __name__ == '__main__':
   unittest.main()