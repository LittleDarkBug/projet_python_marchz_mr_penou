from mongoengine import Document, StringField
from bson import ObjectId

class Fournisseur(Document):
    nom = StringField(required=True)
    adresse = StringField(required=True)
    telephone = StringField(required=True)
    email = StringField(required=True)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'objet.

        Returns:
            str: Une chaîne de caractères détaillant les propriétés de l'objet.
        """
        return (
            f"=== Fournisseur ===\n"
            f"ID: {self.id}\n"
            f"Nom: {self.nom}\n"
            f"Adresse: {self.adresse}\n"
            f"Téléphone: {self.telephone}\n"
            f"Email: {self.email}\n"
            "================="
        )


    @classmethod
    def find(cls, criteria: dict):
        """Recherche des fournisseurs en fonction des critères spécifiés."""
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """Recherche un seul fournisseur en fonction des critères spécifiés."""
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """Recherche un fournisseur par son ID MongoDB."""
        return cls.objects(id=ObjectId(id)).first()
