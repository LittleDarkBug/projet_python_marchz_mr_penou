from mongoengine import Document, StringField, ListField, ReferenceField, IntField
from core.classes.Utilisateur import Utilisateur
from core.enums.TypeMarchandEnum import TypeMarchandEnum
from core.classes.Produit import Produit
from core.utils.PasswordUtils import PasswordUtils
from rich import print

class Marchand(Utilisateur):
    description = StringField()
    type_marchand = StringField(required=True)
    x = IntField(default=0)
    y = IntField(default=0)
    produits = ListField(ReferenceField(Produit), default=[])


    def __str__(self):
        return (
            f"=== Marchand ===\n"
            f"ID: {self.id}\n"
            f"Nom: {self.nom}\n"
            f"Prénom: {self.prenom}\n"
            f"Téléphone: {self.telephone}\n"
            f"Adresse: {self.adresse}\n"
            f"Nom d'utilisateur: {self.username}\n"
            f"Description: {self.description}\n"
            f"Type de marchand: {self.type_marchand}\n"
            f"Position: ({self.x}, {self.y})\n"
            f"Produits: {len(self.produits)} produit(s)\n"
            "================="
        )

    def ajouter_produit(self, produit: Produit) -> None:
        """Ajoute un produit à la liste des produits du marchand."""
        if produit in self.produits:
            raise ValueError("Ce produit est déjà dans la liste du marchand.")
        self.produits.append(produit)
        self.save()  # Sauvegarde après ajout
        print(f"Produit '{produit.libelle}' ajouté avec succès.")

    def retirer_produit(self, produit: Produit) -> None:
        """Retire un produit de la liste des produits du marchand."""
        if produit not in self.produits:
            raise ValueError("Ce produit n'est pas dans la liste du marchand.")
        self.produits.remove(produit)
        self.save()  # Sauvegarde après retrait
        print(f"Produit '{produit.libelle}' retiré avec succès.")

    @property
    def niveau_de_stock(self) -> int:
        """Calcule et retourne le niveau de stock du marchand."""
        return sum(produit.quantite for produit in self.produits)

    @classmethod
    def find(cls, criteria: dict):
        """Recherche des marchands en fonction des critères spécifiés."""
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """Recherche un marchand en fonction des critères spécifiés."""
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """Recherche un marchand par son ID."""
        return cls.objects(id=id).first()

    def save_marchand(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)

    def delete_marchand(self) -> None:
        """Supprime le marchand de la base de données."""
        self.delete()

    def rechercher_produits_par_libelle(self, libelle: str):
        """Recherche des produits par libellé."""
        return [produit for produit in self.produits if produit.libelle.lower() == libelle.lower()]
    
    def rechercher_produit(self , mot_cle: str):
        """Recherche des produits par mot-clé sur tous les attribut d'un produit"""
        champs_recherche = ['libelle', 'description']
        return [produit for produit in self.produits if any(mot_cle.lower() in str(getattr(produit, champ)).lower() for champ in champs_recherche)]
        