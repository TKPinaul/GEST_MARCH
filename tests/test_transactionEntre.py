import unittest
from unittest.mock import MagicMock, patch
from GEST_MARCH.models.marchands import Marchands
from GEST_MARCH.models.transactionEntre import TransactionEntree
from configs.bd_connexion import get_database


class TestTransactionEntree(unittest.TestCase):
   """
      Test des fonctionnalités de la classe TransactionEntree
      1 - Initialisation d'une transaction d'entree
      2 - Augmentation du stock d'un marchand et enregistrement de la transaction
      3 - Ajout de stock a un marchand
      4 - enregistrement de transaction
      5 - recuperation de tous les transaction
      6 - recuperation d'une transaction
      7 - recuperation des transaction d'un marchand
      8 - recuperation des transaction d'un produits
      9 - recuperation des transaction d'un montant minimum
      10 - recuperation des transaction d'un montant maximum
      11 - recuperation des transaction d'un montant (min max)
   """
   
   def setUp(self):
      """Initialise des objets pour le test."""
      self.db_mock = MagicMock()
      self.collection_mock = MagicMock()
      self.patcher = patch('configs.bd_connexion.get_database', return_value=self.db_mock)
      self.patcher.start()
      self.db_mock.__getitem__.return_value = self.collection_mock
      
      self.marchand_data = {
         'code_marchand': '123',
         'nom': 'Marchand Test',
         'stock': {
            'Loup': {'quantite': 10, 'prix_unitaire': 5.0}
         }
      }
      self.marchand_mock = MagicMock()
      self.marchand_mock.code_marchand = self.marchand_data['code_marchand']
      self.marchand_mock.stock = self.marchand_data['stock']
      Marchands.get_one = MagicMock(return_value=self.marchand_data)
      Marchands.from_dict = MagicMock(return_value=self.marchand_mock)
      
   def tearDown(self):
      """Nettoyage apres test"""
      self.patcher.stop()
        
   # 1
   def test_init(self):
      """Test de l'initialisation"""
      transaction = TransactionEntree(
         code_marchand='123',
         nom_produit='Loup',
         quantite_entree=5,
         prix_unitaire=5.0
      )
      
      # Vérifier que les attributs sont correctement initialisés
      self.assertEqual(transaction.code_marchand, '123')
      self.assertEqual(transaction.nom_produit, 'Loup')
      self.assertEqual(transaction.quantite_entree, 5)
      self.assertEqual(transaction.prix_unitaire, 5.0)
      self.assertIsNone(transaction.montant_total)  # montant_total est calculé plus tard
      self.assertIsNotNone(transaction.transaction_id)
      
   # 2
   def test_buy_produit(self):
      """Augmentation du stock d'un marchand"""
      transaction = TransactionEntree(
         code_marchand='123',
         nom_produit='Loup',
         quantite_entree=5,
         prix_unitaire=5.0
      )
      transaction.buy_product()
      
      # Vérifier que le stock du marchand a été mis à jour
      self.marchand_mock.update_stock.assert_called_once()
      self.assertEqual(self.marchand_mock.stock['Loup']['quantite'], 15)
      
      self.assertEqual(transaction.montant_total, 25.0) # Vérifier que le montant total a été calculé correctement
      self.collection_mock.insert_one.assert_called_once()

   # 3


   # 4


   # 5


   # 6


   # 7


   # 8


   # 9


   # 10


   # 11

