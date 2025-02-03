import uuid
import bcrypt
from configs.bd_connexion import get_database
from pymongo.errors import PyMongoError


class Personne:
   """Classe définissant une personne parente de Marchands et Admin"""
   
   TYPES_PERSONNES = ["Client", "Marchand", "Admin"]  # Types de personnes autorisés
    
   def __init__(self, code_id, nom, contact, type_personne=None,  mots_passe=None):
      """Initialisation d'une personne"""
      self.code_id = code_id if code_id else str(uuid.uuid4()) # Générer un id aléatoire si non fourni
      self.nom = nom
      self.contact = contact
      self.type_personne = type_personne if type_personne in self.TYPES_PERSONNES else "Client"
      
      self.__mots_passe = self.__hash_mots_passe(mots_passe) if mots_passe else None # Attribut privé (mots de passe hashé)
      
   def get_mots_passe(self):
      """Retourne le mot de passe (haché)"""
      return self.__mots_passe
 
   def __hash_mots_passe(self, mots_passe):
      """Hache le mot de passe avec bcrypt"""
      if mots_passe:
         if isinstance(mots_passe, str):
            # Générer un salt et hasher le mot de passe
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(mots_passe.encode('utf-8'), salt)
         elif isinstance(mots_passe, bytes):
            return mots_passe
      return None
   
   def save(self, collection_name):
      """Enregistre une personne dans la base de données"""
      db = get_database() # Récupérer la base de données
      collection = db[collection_name] # Récupérer la collection sinon la créer
      
      existing_personne = collection.find_one({'nom': self.nom})
      if existing_personne:
         raise ValueError(f"[bold yellow]Une personne avec le nom '{self.nom}' existe déjà[/bold yellow]")
      
      personne = {
         'code_id': self.code_id,
         'nom': self.nom,
         'contact': self.contact,
         'type_personne': self.type_personne,
         'mots_passe': self.__mots_passe
      }
      try:
         collection.insert_one(personne)
      except PyMongoError as e:
         raise Exception(f"Erreur lors de l'insertion dans la base de données : {e}")
      finally:
         db.client.close()
         
   def verifier_pass(self, mots_passe):
      if self.__mots_passe and mots_passe:
         return bcrypt.checkpw(mots_passe.encode('utf-8'), self.__mots_passe)
      return False
   
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
         if new_type_personne not in self.TYPES_PERSONNES:
            raise ValueError(f"Type de personne invalide : {new_type_personne}")
         new_values['type_personne'] = new_type_personne
      
      try:
         if new_values:
             result = collection.update_one({'code_id': self.code_id}, {'$set': new_values})
             return result.modified_count
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la mise à jour dans la base de données : {e}")
      finally:
         db.client.close()
     
   def delete_personne(self, collection_name):
      """Supprime une personne de la base de données"""
      db = get_database()
      collection = db[collection_name]
      try:
         result = collection.delete_one({'code_id': self.code_id})
         return result.deleted_count
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la suppression dans la base de données : {e}")
      finally:
         db.client.close()
         
   
   @staticmethod
   def get_one(collection_name, code_id):
      """Récupère une personne à partir de son code_id"""
      db = get_database()
      collection = db[collection_name]
      try:
         personne = collection.find_one({'code_id': code_id})
         return personne
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la récupération dans la base de données : {e}")
      finally:
         db.client.close()
   
   @staticmethod
   def get_all():
      """Récupère toutes les personnes"""
      db = get_database()
      try:
         collection = db["personnes"]
         personnes = list(collection.find())
         return personnes
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la récupération dans la base de données : {e}")
      finally:
         db.client.close()
   
   @staticmethod
   def get_by_type(type_personne):
      """Récupère toutes les personnes d'un type donné"""
      db = get_database()
      collection = db["personnes"]
      try:
         personnes = list(collection.find({'type_personne': type_personne}))
         return personnes
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la récupération dans la base de données : {e}")
      finally:
         db.client.close()
   
   @staticmethod
   def get_by_nom(collection_name, nom):
      """Récupère toutes les personnes d'un nom donné"""
      db = get_database()
      collection = db[collection_name]
      try:
         personnes = list(collection.find({'nom': nom}))
         return personnes
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la récupération dans la base de données : {e}")
      finally:
         db.client.close()
   
   @staticmethod
   def get_by_contact(collection_name, contact):
      """Récupère toutes les personnes d'un contact donné"""
      db = get_database()
      collection = db[collection_name]
      try:
         personnes = list(collection.find({'contact': contact}))
         return personnes
      except PyMongoError as e:
         raise Exception(f"Erreur lors de la récupération dans la base de données : {e}")
      finally:
         db.client.close()
         
   @staticmethod
   def from_dict(data):
      """Recree une instance Personne"""
      return Personne(
         code_id=data.get('code_id'),
         nom=data.get('nom'),
         contact=data.get('contact'),
         type_personne=data.get('type_personne'),
         mots_passe=data.get('mots_passe')
      )