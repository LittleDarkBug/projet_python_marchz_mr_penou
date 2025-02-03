from bson import ObjectId
from datetime import datetime
from core.classes.CouponGenerique import CouponGenerique
from mongoengine import Document, BooleanField, DateTimeField, FloatField, StringField, IntField

class CodePromo(CouponGenerique):
    """
    Classe représentant un code promo dans MongoDB avec des fonctionnalités étendues.
    """
    max_usage_per_user = IntField(required=True)
    all_users = BooleanField(required=True)
    code = StringField(required=True, unique=True)



    def is_valid(self) -> bool:
        """Retourne True si le code promo est valide."""
        return self.actif and (self.date_expiration > datetime.now())

    def apply_discount(self, montant: float) -> float:
        """Applique la réduction sur un montant donné."""
        if self.reduction_montant:
            return montant - self.reduction_montant
        elif self.reduction_taux:
            return montant * (1 - self.reduction_taux / 100)
        return montant

    def usage_limit_reached(self, usage_count: int) -> bool:
        """Vérifie si le nombre d'utilisations est atteint."""
        return usage_count >= self.max_usage_per_user

    def is_applicable_to_user(self, user_id: str) -> bool:
        """Vérifie si le code promo est applicable à un utilisateur donné."""
        if self.all_users:
            return True
        return False

    def save(self) -> None:
        """Sauvegarde le code promo dans MongoDB."""
        super().save()

    def delete(self) -> None:
        """Supprime le code promo de MongoDB."""
        if self.id:
            self.delete()
        else:
            raise ValueError("Impossible de supprimer un code promo sans ID.")

    @classmethod
    def find(cls, criteria: dict):
        """Recherche des codes promo avec critères."""
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """Recherche un seul code promo avec critères."""
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """Recherche un code promo par ID."""
        return cls.objects(id=ObjectId(id)).first()
