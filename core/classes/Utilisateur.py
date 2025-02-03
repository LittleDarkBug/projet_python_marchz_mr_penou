from mongoengine import Document, StringField
from core.utils.PasswordUtils import PasswordUtils

class Utilisateur(Document):
    nom = StringField(required=True)
    prenom = StringField(required=True)
    telephone = StringField(required=True)
    adresse = StringField(required=True)
    description = StringField()
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

    meta = {'allow_inheritance': True}

    def save(self, *args, **kwargs):
        """Hache le mot de passe avant de sauvegarder."""
        if not self.pk:  # Seulement lors de la création
            self.password = str(PasswordUtils.hash_password(self.password))
        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"=== Utilisateur ===\n"
            f"ID: {self.id}\n"
            f"Nom: {self.nom}\n"
            f"Prénom: {self.prenom}\n"
            f"Téléphone: {self.telephone}\n"
            f"Adresse: {self.adresse}\n"
            f"Pseudo: {self.username}\n"
            f"Description: {self.description}\n"
            "================="
        )

    @classmethod
    def find(cls, criteria: dict):
        """Recherche plusieurs utilisateurs selon un critère."""
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """Recherche un utilisateur unique selon un critère."""
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """Recherche un utilisateur par son ID."""
        return cls.objects(id=id).first()

    def delete(self, *args, **kwargs):
        """Supprime l'utilisateur de la base de données."""
        super().delete(*args, **kwargs)
