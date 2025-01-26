import unittest

from configs.bd_connexion import get_database
from GEST_MARCH.models.personne import Personne


class TestPersonne(unittest.TestCase):
   """
   Test des fonctionnaliter de la class personne
   1 - l'initialisation d'une personne
   2 - Enregistrement d'une personne
   3 - Mise à jour d'une personne
   4 - Suppression d'une personne
   5 - Récupération d'une personne par son id
   6 - Récupération de toutes les personnes
   7 - Récupération de toutes les personnes d'un type donné
   8 - Récupération de toutes les personnes d'un nom donné
   9 - Récupération de toutes les personnes d'un contact donné
   """
   
   def setUp(self):
      """Initialise des objets pour le test."""
      self.personne = Personne(
         code_id=None,
         nom = "Personne Test",
         contact = "00000000",
         type_personne = "Client"
      )
      try:
         self.db = get_database() # Récupérer la base de données
         self.collection = self.db['personnes'] # Récupérer la collection
      except Exception as e: # Gérer les exceptions en cas d'erreur de connexion
         raise Exception(f"La connexion à la base de données a échoué : {e}")
      
   def tearDown(self):
      """Nettoyage de la bd apres test"""
      self.collection.delete_many({}) # Supprimer tous les documents de la collection
      self.db.client.close() # Fermer la connexion
      
   # 1
   def test_init(self):
      """Test de l'initialisation"""
      self.assertEqual(self.personne.nom, "Personne Test")
      self.assertEqual(self.personne.contact, "00000000")
      self.assertEqual(self.personne.type_personne, "Client")
      self.assertIsNotNone(self.personne.code_id) # Vérifier si l'id est généré
      
   # 2
   def test_save(self):
      """Test d'enregistrement d'une personne"""
      if not self.db is None:
         self.skipTest("Connexion à la base de données échouée.")
      
      self.personne.save('personnes') # Enregistrer la personne
      personne_save = self.collection.find_one({'code_id' : self.personne.code_id}) # Récupérer la personne enregistrée
      
      self.assertIsNotNone(personne_save)
      self.assertEqual(personne_save['nom'], "Personne Test")
      self.assertEqual(personne_save['contact'], "00000000")
      self.assertEqual(personne_save['type_personne'], "Client")
      
   # 3
   def test_update_personne(self):
      """Test de mise à jour d'une personne"""
      if not self.db is None:
         self.skipTest("Connexion à la base de données échouée.")
      
      self.personne.save('personnes') # Enregistrer la personne
      data = self.personne.update_personne(
         'personnes',
         new_nom="Personne Test 2", 
         new_contact="11111111", 
         new_type_personne="Marchand"
      ) # Mettre à jour la personne
      
      self.assertEqual(data, 1) # Vérifier si la mise à jour a été effectuée
      personne_updated = self.collection.find_one({'code_id' : self.personne.code_id}) # Récupérer la personne mise à jour
      
      self.assertIsNotNone(personne_updated) # Vérifier si la personne existe
      self.assertEqual(personne_updated['nom'], "Personne Test 2") # Vérifier si le nom a été mis à jour
      self.assertEqual(personne_updated['contact'], "11111111")  # Vérifier si le contact a été mis à jour
      self.assertEqual(personne_updated['type_personne'], "Fournisseur") # Vérifier si le type de personne a été mis à jour
      
   # 4
   def test_delete_personne(self):
      """Test de suppression d'une personne"""
      if not self.db is None:
         self.skipTest("Connexion à la base de données échouée.")
      
      self.personne.save('personnes')
      data = self.personne.delete_personne('personnes') # Supprimer la personne
      
      personne_deleted = self.collection.find_one({'code_id' : self.personne.code_id}) # Récupérer la personne supprimée
      self.assertIsNone(personne_deleted) # Vérifier si la personne n'existe plus
      
   # 5
   def test_get_one(self):
      """Test de récupération d'une personne par son id"""
      if not self.db is None:
         self.skipTest("Connexion à la base de données échouée.")
      
      self.personne.save('personnes')
      personne = Personne.get_one('personnes', self.personne.code_id) # Récupérer la personne
      
      self.assertIsNotNone(personne)
      self.assertEqual(personne['nom'], "Personne Test")
      self.assertEqual(personne['contact'], "00000000")
      self.assertEqual(personne['type_personne'], "Client")
      
   # 6
   def test_get_all(self):
      """Test de récupération de toutes les personnes"""
      if not self.db is None:
         self.skipTest("Connexion à la base de données échouée.")
      
      self.personne.save('personnes')
      personnes = Personne.get_all('personnes') # Récupérer toutes les personnes
      
      self.assertIsNotNone(personnes)
      personnes = list(Personne.get_all('personnes'))
      self.assertEqual(personnes[0]['nom'], "Personne Test")
      
   # 7
   def test_get_by_type(self):
      """Test de récupération de toutes les personnes d'un type donné"""
      if not self.db is None:
         self.skipTest("Connexion à la base de données échouée.")
      
      self.personne.save('personnes')
      personnes = Personne.get_by_type('personnes', 'Client') # Récupérer toutes les personnes du type Client
      self.assertEqual(len(personnes), 1) # Vérifier si une seule personne a été récupérée
      
   # 8
   def test_get_by_nom(self):
      """Test de récupération de toutes les personnes d'un nom donné"""
      if not self.db is None:
         self.skipTest("Connexion à la base de données échouée.")
      
      self.personne.save('personnes')
      personnes = list(Personne.get_by_nom('personnes', 'Personne Test')) # Récupérer toutes les personnes du nom "Personne Test"
      self.assertEqual(len(personnes), 1) # Vérifier si une seule personne a été récupérée
      self.assertEqual(personnes[0]['nom'], "Personne Test") # Vérifier si le nom de la personne est correct
      
   # 9
   def test_get_by_contact(self):
      """Test de récupération de toutes les personnes d'un contact donné"""
      if not self.db is None:
         self.skipTest("Connexion à la base de données échouée.")
      
      self.personne.save('personnes')
      personnes = list(Personne.get_by_contact('personnes', '00000000')) # Récupérer toutes les personnes du contact "00000000"
      self.assertEqual(len(personnes), 1) # Vérifier si une seule personne a été récupérée
      self.assertEqual(personnes[0]['contact'], "00000000") # Vérifier si le contact de la personne est correct
      
if __name__ == "__main__":
   unittest.main() # Exécutez les tests