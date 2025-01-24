from GEST_MARCH.models.personne import Personne


class Admin(Personne):
   def __init__(self, code_id, nom, contact, type_personne="Admin"):
      """Initialisation d'un administrateur"""
      super().__init__(code_id, nom, contact, type_personne)
      
   def save(self):
      """Enregistre un administrateur dans la base de données"""
      super().save("admins") # Enregistrer l'administrateur dans la collection admins