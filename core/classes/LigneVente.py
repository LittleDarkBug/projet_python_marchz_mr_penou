from mongoengine import Document, FloatField, IntField, ReferenceField
from core.classes.Produit import Produit

class LigneVente(Document):
    quantite = IntField(required=True)
    prix_total_ligne = FloatField(required=True)
    produit = ReferenceField(Produit, required=True)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'objet.

        Returns:
            str: Une chaîne de caractères détaillant les propriétés de la ligne de vente.
        """
        return (
            f"=== Ligne de Vente ===\n"
            f"ID: {self.id}\n"
            f"Quantité: {self.quantite}\n"
            f"Produit: {self.produit.libelle}\n"
            f"Prix total de la ligne: {self.prix_total_ligne:.2f} €\n"
            "======================"
        )

    @classmethod
    def find(cls, criteria: dict):
        """Recherche des lignes de vente en fonction des critères spécifiés."""
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """Recherche une ligne de vente en fonction des critères spécifiés."""
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """Recherche une ligne de vente par son ID."""
        return cls.objects(id=id).first()

    def save_ligne_vente(self) -> None:
        """Sauvegarde la ligne de vente dans la base de données."""
        self.save()

    def delete_ligne_vente(self) -> None:
        """Supprime la ligne de vente de la base de données."""
        self.delete()
