from core.classes.Utilisateur import Utilisateur
from typing import List
from mongoengine import Document, StringField, BooleanField, ListField, ReferenceField
from core.utils.PasswordUtils import PasswordUtils

class Admin(Utilisateur):

    def __str__(self):
        return (
            f"=== Admin ===\n"
            f"ID: {self.id}\n"
            f"Nom d'utilisateur: {self.username}\n"
            "================="
        )

    
