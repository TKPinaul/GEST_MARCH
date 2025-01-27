import unittest
from configs.bd_connexion import get_database
from GEST_MARCH.models.marchands import Marchands
from GEST_MARCH.models.marche import Marche


class TestMarchands(unittest.TestCase):
   """
   Test des fonctionnalités de la classe Marchands.
   1 - Initialisation d'un marchand
   2 - Enregistrement d'un marchand
   3 - Mise à jour de la quantité d'un produit
   4 - Mise à jour du prix d'un produit
   5 - Occupation d'un stand dans un marché
   6 - Changement de stand dans un marché
   7 - Suppression d'un marchand
   8 - Récupération d'un marchand par son ID
   9 - Récupération de tous les marchands
   """

   def setUp(self):
      """Initialise des objets pour le test."""
      self.marchand = Marchands(
         nom = "Marchand Test",
         contact = "00000000",
         coordonneeX = 0,
         coordonneeY = 0,
         stock = {"produit1": {"quantite": 10, "prix_unitaire": 5.0}}
      ) # Initialisation d'un marchand
      self.marche = Marche(
         nom_marche = "Marché Test", 
         x_ligne = 10, 
         y_colonne = 10) # Initialisation d'un marché
      try:
         self.db = get_database()
         self.collection_marchands = self.db['marchands']
         self.collection_marches = self.db['marches']
      except Exception as e:
         raise Exception(f"La connexion à la base de données a échoué : {e}")

   def tearDown(self):
      """Nettoyage de la base de données après chaque test."""
      self.collection_marchands.delete_many({})  # Supprimer tous les documents de la collection marchands
      self.collection_marches.delete_many({})  # Supprimer tous les documents de la collection marches
      self.db.client.close()  # Fermer la connexion

   # 1
   def test_init(self):
      """Test de l'initialisation d'un marchand."""
      self.assertEqual(self.marchand.nom, "Marchand Test", "Le nom du marchand est incorrect.")
      self.assertEqual(self.marchand.contact, "00000000", "Le contact du marchand est incorrect.")
      self.assertEqual(self.marchand.coordonneeX, 0, "La coordonnée X du marchand est incorrecte.")
      self.assertEqual(self.marchand.coordonneeY, 0, "La coordonnée Y du marchand est incorrecte.")
      self.assertEqual(self.marchand.stock["produit1"]["quantite"], 10, "La quantité du produit est incorrecte.")
      self.assertEqual(self.marchand.stock["produit1"]["prix_unitaire"], 5.0, "Le prix unitaire du produit est incorrect.")

   # 2
   def test_save(self):
      """Test d'enregistrement d'un marchand."""
      if self.db is None:
         self.skipTest("Connexion à la base de données échouée.")

      self.marchand.save()
      marchand_save = self.collection_marchands.find_one({'code_id': self.marchand.code_id})
      self.assertIsNotNone(marchand_save, "Le marchand n'a pas été enregistré.")
      self.assertEqual(marchand_save['nom'], "Marchand Test", "Le nom du marchand enregistré est incorrect.")
      self.assertEqual(marchand_save['contact'], "00000000", "Le contact du marchand enregistré est incorrect.")
      self.assertEqual(marchand_save['coordonneeX'], 0, "La coordonnée X du marchand enregistré est incorrecte.")
      self.assertEqual(marchand_save['coordonneeY'], 0, "La coordonnée Y du marchand enregistré est incorrecte.")

   # 3
   def test_update_quantite(self):
      """Test de la mise à jour de la quantité d'un produit."""
      self.marchand.update_quantite("produit1", 20)
      self.assertEqual(self.marchand.stock["produit1"]["quantite"], 20, "La quantité du produit n'a pas été mise à jour.")

      with self.assertRaises(ValueError, msg="La mise à jour d'un produit inexistant devrait lever une exception."):
         self.marchand.update_quantite("produit2", 30)

   # 4
   def test_update_prix(self):
      """Test de la mise à jour du prix d'un produit."""
      self.marchand.update_prix("produit1", 10.0)
      self.assertEqual(self.marchand.stock["produit1"]["prix_unitaire"], 10.0, "Le prix unitaire du produit n'a pas été mis à jour.")

      with self.assertRaises(ValueError, msg="La mise à jour d'un produit inexistant devrait lever une exception."):
         self.marchand.update_prix("produit2", 15.0)

   # 5
   def test_occup_stand(self):
      """Test de l'occupation d'un stand dans un marché."""
      self.marchand.occup_stand(self.marche)
      self.assertTrue(self.marche.grille[0][0], "Le stand (0, 0) devrait être occupé.")

      with self.assertRaises(ValueError, msg="L'occupation d'un stand déjà occupé devrait lever une exception."):
         self.marchand.occup_stand(self.marche)

   # 6
   def test_change_stand(self):
      """Test du changement de stand dans un marché."""
      self.marchand.occup_stand(self.marche)
      self.marchand.change_stand(self.marche, 1, 1)
      self.assertFalse(self.marche.grille[0][0], "L'ancien stand (0, 0) devrait être libéré.")
      self.assertTrue(self.marche.grille[1][1], "Le nouveau stand (1, 1) devrait être occupé.")

      with self.assertRaises(ValueError, msg="Le changement vers un stand déjà occupé devrait lever une exception."):
         self.marchand.change_stand(self.marche, 1, 1)

   # 7
   def test_delete_marchand(self):
      """Test de la suppression d'un marchand."""
      if self.db is None:
         self.skipTest("Connexion à la base de données échouée.")

      self.marchand.save()
      self.marchand.occup_stand(self.marche)
      deleted_count = self.marchand.delete_marchand(self.marche)
      self.assertEqual(deleted_count, 1, "Le marchand n'a pas été supprimé.")
      self.assertFalse(self.marche.grille[0][0], "Le stand (0, 0) devrait être libéré après la suppression du marchand.")

   # 8
   def test_get_one(self):
      """Test de la récupération d'un marchand par son ID."""
      if self.db is None:
         self.skipTest("Connexion à la base de données échouée.")

      self.marchand.save()
      marchand_recupere = Marchands.get_one(self.marchand.code_id)
      self.assertIsNotNone(marchand_recupere, "Le marchand devrait être récupéré.")
      self.assertEqual(marchand_recupere['nom'], "Marchand Test", "Le nom du marchand récupéré est incorrect.")
      self.assertEqual(marchand_recupere['contact'], "00000000", "Le contact du marchand récupéré est incorrect.")

   # 9
   def test_get_all(self):
      """Test de la récupération de tous les marchands."""
      if self.db is None:
         self.skipTest("Connexion à la base de données échouée.")

      self.marchand.save()
      marchands = Marchands.get_all()
      self.assertEqual(len(list(marchands)), 1, "Un seul marchand devrait être récupéré.")


if __name__ == '__main__':
   unittest.main()  # Exécutez les tests