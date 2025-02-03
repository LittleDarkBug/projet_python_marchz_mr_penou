from mongoengine import Document, FloatField, IntField, ReferenceField, ListField, StringField
from core.classes.CouponGenerique import CouponGenerique
from core.classes.Fournisseur import Fournisseur
from core.enums.TypeUniteEnum import TypeUniteEnum

class Produit(Document):
    libelle = StringField(required=True)
    prix_achat = FloatField(required=True)
    prix_vente = FloatField(required=True)
    description = StringField()
    type_unite = StringField(choices=[type.name for type in TypeUniteEnum], default=TypeUniteEnum.UNITAIRE.name)
    quantite = IntField(required=True)
    fournisseur = ReferenceField(Fournisseur)
    coupons = ListField(ReferenceField(CouponGenerique))

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'objet.

        Returns:
            str: Une chaîne de caractères détaillant les propriétés de l'objet.
        """
        return (
            f"=== Produit ===\n"
            f"ID: {self.id}\n"
            f"Libellé: {self.libelle}\n"
            f"Prix d'achat: {self.prix_achat:.2f} FCFA\n"
            f"Prix de vente: {self.prix_vente:.2f} FCFA\n"
            f"Description: {self.description}\n"
            f"Type d'unité: {self.type_unite}\n"
            f"Quantité: {self.quantite}\n"
            f"Fournisseur: {self.fournisseur}\n"
            f"Coupons associés: {len(self.coupons)} coupon(s)\n"
            "================="
        )

    def ajouter_coupon(self, coupon) -> None:
        """
        Ajoute un coupon au produit et met à jour la relation bidirectionnelle.

        Args:
            coupon (CouponGenerique): Le coupon à ajouter.
        """
        if coupon not in self.coupons:
            self.coupons.append(coupon)
            if self not in coupon.produits:
                coupon.ajouter_produit(self)

    def retirer_coupon(self, coupon) -> None:
        """
        Retire un coupon du produit et met à jour la relation bidirectionnelle.

        Args:
            coupon (CouponGenerique): Le coupon à retirer.
        """
        if coupon in self.coupons:
            self.coupons.remove(coupon)
            if self in coupon.produits:
                coupon.retirer_produit(self)


    @classmethod
    def find(cls, criteria: dict):
        """Recherche des produits en fonction des critères spécifiés."""
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """Recherche un seul produit en fonction des critères spécifiés."""
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """Recherche un produit par son ID MongoDB."""
        return cls.objects(id=id).first()
