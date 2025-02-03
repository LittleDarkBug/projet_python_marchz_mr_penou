from datetime import date
from typing import List, Optional
from mongoengine import Document, BooleanField, FloatField, DateField, ListField, ReferenceField
from bson import ObjectId


class CouponGenerique(Document):
    """
    Classe représentant un coupon générique dans MongoDB.
    Utilise MongoEngine pour la persistance des données.
    """

    actif = BooleanField(required=True)
    cumulable = BooleanField(required=True)
    date_expiration = DateField(required=True)
    reduction_montant = FloatField(required=True)
    reduction_taux = FloatField(required=True)
    global_coupon = BooleanField(required=True)

    meta = {
        'collection': 'coupons_generiques'  # Nom de la collection dans MongoDB
    }

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'objet.
        """
        return (
            f"=== Coupon ===\n"
            f"ID: {self.id}\n"
            f"Actif: {'Oui' if self.actif else 'Non'}\n"
            f"Cumulable: {'Oui' if self.cumulable else 'Non'}\n"
            f"Date d'expiration: {self.date_expiration}\n"
            f"Réduction (montant): {self.reduction_montant}\n"
            f"Réduction (taux): {self.reduction_taux}\n"
            f"Coupon global: {'Oui' if self.global_coupon else 'Non'}\n"
            "================="
        )


    @classmethod
    def find(cls, criteria: dict):
        """
        Recherche des coupons génériques en fonction des critères spécifiés.
        """
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """
        Recherche un seul coupon générique en fonction des critères spécifiés.
        """
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """
        Recherche un coupon générique par son ID MongoDB.
        """
        return cls.objects(id=ObjectId(id)).first()
