from mongoengine import Document, StringField, ObjectIdField
from core.utils.PasswordUtils import PasswordUtils

class CategorieProduit(Document):
    """
    Classe représentant une catégorie de produit dans MongoDB.
    """
    libelle = StringField(required=True)
    description = StringField(required=True)
    
    meta = {
        'collection': 'categories'  # Nom de la collection MongoDB
    }

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'objet.
        """
        return (
            f"=== Catégorie ===\n"
            f"ID: {self.id}\n"
            f"Libellé: {self.libelle}\n"
            f"Description: {self.description}\n"
            "================="
        )

    def save(self) -> None:
        """
        Sauvegarde la catégorie dans la base de données MongoDB.
        Si l'ID existe, il met à jour la catégorie. Sinon, il crée une nouvelle catégorie.
        """
        super().save()

    def delete(self) -> None:
        """
        Supprime la catégorie de la base de données MongoDB.
        """
        if self.id:
            self.delete()
        else:
            raise ValueError("Impossible de supprimer une catégorie sans ID.")

    @classmethod
    def find(cls, criteria: dict):
        """
        Recherche des catégories en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.

        Returns:
            QuerySet: Un objet QuerySet MongoEngine pour parcourir les documents trouvés.
        """
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """
        Recherche une seule catégorie en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.

        Returns:
            CategorieProduit: L'objet CategorieProduit trouvé, ou None si aucune catégorie n'est trouvée.
        """
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """
        Recherche une catégorie par son ID MongoDB.

        Args:
            id (str): L'ID MongoDB de la catégorie à rechercher.

        Returns:
            CategorieProduit: L'objet CategorieProduit trouvé, ou None si aucune catégorie n'est trouvée.
        """
        return cls.objects(id=id).first()
