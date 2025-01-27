import unittest
import io
import sys

from configs.bd_connexion import get_database
from GEST_MARCH.models.marche import Marche


class TestMarche(unittest.TestCase):
   """
   Test des fonctionnaliter de la class march
   1 - l'initialisation
   2 - Enregistrement d'un marche
   3 - Disponibiliter des stand
   4 - Occuper un stand
   5 - liberer un stand
   6 - visualisation de la grille
   7 - recuperation de tout les marche
   8 - recuperation d'un marche par son id
   """

   def setUp(self):
      """Initialise des objets pour le test."""
      self.marche = Marche(
         nom_marche = "Marché Test",
         x_ligne = 10,
         y_colonne = 10
      )
      try:
         self.db = get_database()
         self.collection = self.db['marches']
      except Exception as e:
         raise Exception(f"La connexion à la base de données a échoué : {e}")

   def tearDown(self):
      """Nettoyage de la bd apres test"""
      try:
         self.collection.delete_many({})  # supprimer tous les documents de la collection
         self.db.client.close()  # fermer la connexion
      except Exception as e:
         raise Exception(f"Erreur lors de la suppression des données de test : {e}")

   # 1
   def test_init(self):
      """Test de l'initialisation"""
      self.assertEqual(self.marche.nom_marche, "Marché Test", "Le nom du marché est incorrect.")
      self.assertEqual(self.marche.x_ligne, 10, "Le nombre de lignes est incorrect.")
      self.assertEqual(self.marche.y_colonne, 10, "Le nombre de colonnes est incorrect.")
      self.assertEqual(len(self.marche.grille), 10, "La grille n'a pas le bon nombre de lignes.")
      self.assertEqual(len(self.marche.grille[0]), 10, "La grille n'a pas le bon nombre de colonnes.")
      self.assertFalse(any(any(stand for stand in ligne) for ligne in self.marche.grille), "La grille ne devrait pas contenir de stands occupés.")
        
   # 2
   def test_save(self):
      """Test d'enregistrement d'un marche"""
      if self.db is None:
        self.skipTest("Connexion à la base de données échouée.")
      
      self.marche.save()
      marche_save = self.collection.find_one({'marche_id' : self.marche.marche_id})
      
      self.assertIsNotNone(marche_save, "Le marché n'a pas été enregistré.")
      self.assertEqual(marche_save['nom_marche'], "Marché Test", "Le nom du marché enregistré est incorrect.")
      self.assertEqual(marche_save['x_ligne'], 10, "Le nombre de lignes du marché enregistré est incorrect.")
      self.assertEqual(marche_save['y_colonne'], 10, "Le nombre de colonnes du marché enregistré est incorrect.")

   # 3
   def test_standAvailable(self):
      """Teste la disponibilité d'un stand."""
      self.assertTrue(self.marche.stand_available(0, 0), "Le stand (0, 0) devrait être disponible.")
      self.marche.grille[0][0] = True  # Occuper le stand
      self.assertFalse(self.marche.stand_available(0, 0), "Le stand (0, 0) devrait être occupé.")

      with self.assertRaises(ValueError, msg="Un stand hors de la grille devrait lever une exception."):
         self.marche.stand_available(12, 12)

   # 4 
   def test_occup_stand(self):
      """Teste l'occupation d'un stand."""
      self.marche.occup_stand(0, 0) # occuper un stand
      self.assertTrue(self.marche.grille[0][0], "Le stand (0, 0) devrait être occupé après l'appel à `occup_stand`.")

      with self.assertRaises(ValueError, msg="L'occupation d'un stand déjà occupé devrait lever une exception."): # occuper un stand déjà occupé
         self.marche.occup_stand(0, 0)

      with self.assertRaises(ValueError, msg="L'occupation d'un stand hors de la grille devrait lever une exception."): # occuper un stand hors de la grille
         self.marche.occup_stand(12, 12)

   # 5
   def test_free_stand(self):
      """Teste la libération d'un stand."""
      self.marche.occup_stand(0, 0)
      self.marche.free_stand(0, 0)
      self.assertFalse(self.marche.grille[0][0], "Le stand (0, 0) devrait être libéré après l'appel à `free_stand`.")

      with self.assertRaises(ValueError, msg="La libération d'un stand hors de la grille devrait lever une exception."): # libérer un stand hors de la grille
         self.marche.free_stand(10, 10)

   # 6
   def test_show_grille(self):
      """Teste l'affichage de la grille."""
      captured_output = io.StringIO()
      sys.stdout = captured_output
      self.marche.show_grille()
      sys.stdout = sys.__stdout__
      output = captured_output.getvalue()
      self.assertIn("O", output, "La grille devrait contenir des 'O' pour les stands libres.")

   # 7
   def test_get_all(self):
      """Teste la récupération de tout les marchés."""
      if self.db is None:
        self.skipTest("Connexion à la base de données échouée.")
      
      # Créer et sauvegarder deux marchés
      marche1 = Marche(nom_marche="Marché 1", x_ligne=10, y_colonne=10)
      marche2 = Marche(nom_marche="Marché 2", x_ligne=20, y_colonne=20)
      marche1.save()
      marche2.save()

      marches = Marche.get_all() # Récupérer tous les marchés
      self.assertEqual(len(marches), 2, "Deux marchés devraient être récupérés.")
      
      # Vérifier les noms des marchés récupérés
      noms_marches = [marche['nom_marche'] for marche in marches]
      self.assertIn("Marché 1", noms_marches, "Le marché 'Marché 1' devrait être récupéré.")
      self.assertIn("Marché 2", noms_marches, "Le marché 'Marché 2' devrait être récupéré.")
      
      # Vérifier les dimensions des marchés récupérés
      dimensions_marches = [(marche['x_ligne'], marche['y_colonne']) for marche in marches]
      self.assertIn((10, 10), dimensions_marches, "Les dimensions du marché 'Marché 1' sont incorrectes.")
      self.assertIn((20, 20), dimensions_marches, "Les dimensions du marché 'Marché 2' sont incorrectes.")
   
   # 8
   def test_get_one(self):
      """Teste la récupération d'un marché par son ID."""
      if self.db is None:
        self.skipTest("Connexion à la base de données échouée.")
        
      self.marche.save()
      marche_recupere = Marche.get_one(self.marche.marche_id)
      
      self.assertIsNotNone(marche_recupere, "Le marché devrait être récupéré.")
      self.assertEqual(marche_recupere['nom_marche'], "Marché Test", "Le nom du marché récupéré est incorrect.")
      self.assertEqual(marche_recupere['x_ligne'], 10, "Le nombre de lignes du marché récupéré est incorrect.")
      self.assertEqual(marche_recupere['y_colonne'], 10, "Le nombre de colonnes du marché récupéré est incorrect.")


if __name__ == '__main__':
   unittest.main()