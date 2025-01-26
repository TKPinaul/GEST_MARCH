import uuid

from configs.bd_connexion import get_database


class Personne:
   """Classe définissant une personne parente de Marchands et Admin"""
   
   TYPES_PERSONNES = ["Client", "Marchand", "Admin"]  # Types de personnes autorisés
    
   def __init__(self, code_id, nom, contact, type_personne="Client"):
      """Initialisation d'une personne"""
      self.code_id = code_id if code_id else str(uuid.uuid4()) # Générer un id aléatoire si non fourni
      self.nom = nom
      self.contact = contact
      self.type_personne = type_personne if type_personne in self.TYPES_PERSONNES else "Client"
      
   def save(self, collection_name):
      """Enregistre une personne dans la base de données"""
      db = get_database() # Récupérer la base de données
      collection = db[collection_name] # Récupérer la collection sinon la créer
      personne = {
         'code_id': self.code_id,
         'nom': self.nom,
         'contact': self.contact,
         'type_personne': self.type_personne
      }
      collection.insert_one(personne) # Insérer la personne dans la base de données
      
   def update_personne(self, collection_name, new_nom=None, new_contact=None, new_type_personne=None):
      """Met à jour des informations d'une personne"""
      db = get_database()
      collection = db[collection_name]
      new_values = {} # Nouvelles valeurs à mettre à jour
      if new_nom:
         new_values['nom'] = new_nom
      if new_contact:
         new_values['contact'] = new_contact
      if new_type_personne:
         new_values['type_personne'] = new_type_personne
      
      if new_values:
         result = collection.update_one({'code_id': self.code_id}, {'$set': new_values}) # Mettre à jour la personne
         return result.modified_count
      return 0 # Aucune modification effectuée
   
   def delete_personne(self, collection_name):
      """Supprime une personne de la base de données"""
      db = get_database()
      collection = db[collection_name]
      result = collection.delete_one({'code_id': self.code_id}) # Supprimer une personne
      return result.deleted_count
   
   @staticmethod
   def get_one(collection_name, code_id):
      """Récupère une personne à partir de son code_id"""
      db = get_database()
      collection = db[collection_name]
      personne = collection.find_one({'code_id': code_id}) # Récupérer la personne
      return personne
   
   @staticmethod
   def get_all(collection_name):
      """Récupère toutes les personnes"""
      db = get_database()
      collection = db[collection_name]
      personnes = collection.find() # Récupérer toutes les personnes
      return personnes
   
   @staticmethod
   def get_by_type(collection_name, type_personne):
      """Récupère toutes les personnes d'un type donné"""
      db = get_database()
      collection = db[collection_name]
      personnes = collection.find({'type_personne': type_personne}) # Récupérer toutes les personnes d'un type donné
      return personnes
   
   @staticmethod
   def get_by_nom(collection_name, nom):
      """Récupère toutes les personnes d'un nom donné"""
      db = get_database()
      collection = db[collection_name]
      personnes = collection.find({'nom': nom}) # Récupérer toutes les personnes d'un nom donné
      return personnes
   
   @staticmethod
   def get_by_contact(collection_name, contact):
      """Récupère toutes les personnes d'un contact donné"""
      db = get_database()
      collection = db[collection_name]
      personnes = collection.find({'contact': contact}) # Récupérer toutes les personnes d'un contact donné
      return personnes