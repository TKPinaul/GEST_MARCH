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
   5 - Changement de stand dans un marché
   6 - Suppression d'un marchand
   7 - Récupération d'un marchand par son ID
   8 - Récupération de tous les marchands
   """

   @classmethod
   def setUpClass(cls):
      """Initialisation de la connexion à la base de données."""
      try:
         cls.db = get_database()
         cls.collection_marchands = cls.db['marchands']
         cls.collection_marches = cls.db['marches']
      except Exception as e:
         raise Exception(f"Échec de la connexion à la base de données : {e}")

   def setUp(self):
      """Initialise des objets avant chaque test."""
      self.marche = Marche(nom_marche="Marché Test", x_ligne=10, y_colonne=10)
      self.marche.save()
      self.marche_id = self.marche.marche_id

      self.marchand = Marchands(
         nom="Marchand Test",
         contact="00000000",
         coordonneeX=0,
         coordonneeY=0,
         stock={"produit1": {"quantite": 10, "prix_unitaire": 5.0}}
      )

   def tearDown(self):
      """Nettoyage après chaque test."""
      self.collection_marchands.delete_many({})
      self.collection_marches.delete_many({})

   @classmethod
   def tearDownClass(cls):
      """Fermeture de la connexion à la base de données après tous les tests."""
      cls.db.client.close()

   def test_init(self):
      """Test de l'initialisation d'un marchand."""
      self.assertEqual(self.marchand.nom, "Marchand Test")
      self.assertEqual(self.marchand.contact, "00000000")
      self.assertEqual(self.marchand.coordonneeX, 0)
      self.assertEqual(self.marchand.coordonneeY, 0)
      self.assertEqual(self.marchand.stock["produit1"]["quantite"], 10)
      self.assertEqual(self.marchand.stock["produit1"]["prix_unitaire"], 5.0)

   def test_save(self):
      """Test de l'enregistrement d'un marchand."""
      self.marchand.save(self.marche_id)
      marchand_save = self.collection_marchands.find_one({'code_id': self.marchand.code_id})
      self.assertIsNotNone(marchand_save)
      self.assertEqual(marchand_save['nom'], "Marchand Test")

   def test_update_quantite(self):
      """Test de la mise à jour de la quantité d'un produit."""
      self.marchand.update_quantite("produit1", 20)
      self.assertEqual(self.marchand.stock["produit1"]["quantite"], 20)

      with self.assertRaises(ValueError):
         self.marchand.update_quantite("produit2", 30)

   def test_update_prix(self):
      """Test de la mise à jour du prix d'un produit."""
      self.marchand.update_prix("produit1", 10.0)
      self.assertEqual(self.marchand.stock["produit1"]["prix_unitaire"], 10.0)

      with self.assertRaises(ValueError):
         self.marchand.update_prix("produit2", 15.0)

   def test_change_stand(self):
      """Test du changement de stand."""
      self.marchand.save(self.marche_id)
      self.marchand.change_stand(self.marche, 1, 1)
      self.assertEqual(self.marchand.coordonneeX, 1)
      self.assertEqual(self.marchand.coordonneeY, 1)

   def test_delete_marchand(self):
      """Test de la suppression d'un marchand."""
      self.marchand.save(self.marche_id)
      deleted_count = self.marchand.delete_marchand(self.marche)
      self.assertEqual(deleted_count, 1)

   def test_get_one(self):
      """Test de la récupération d'un marchand par son ID."""
      self.marchand.save(self.marche_id)
      marchand_recupere = Marchands.get_one(self.marchand.code_id)
      self.assertIsNotNone(marchand_recupere)
      self.assertEqual(marchand_recupere['nom'], "Marchand Test")

   def test_get_all(self):
      """Test de la récupération de tous les marchands."""
      self.marchand.save(self.marche_id)
      marchands = Marchands.get_all()
      self.assertGreaterEqual(len(list(marchands)), 1)


if __name__ == '__main__':
   unittest.main()  # Exécutez les tests