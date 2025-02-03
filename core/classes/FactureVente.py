from typing import List
from mongoengine import Document, StringField, DateTimeField, FloatField, ListField, ReferenceField
from datetime import datetime
from core.enums.ModaliteVenteEnum import ModaliteVenteEnum
from core.classes.LigneVente import LigneVente
from core.classes.Utilisateur import Utilisateur
from bson import ObjectId

class FactureVente(Document):
    prix_total = FloatField(required=True)
    numero_vente = StringField(required=True, unique=True)
    date_vente = DateTimeField(required=True)
    modalite = StringField(required=True)  # Enregistrer le nom de l'énumération
    lignes = ListField(ReferenceField(LigneVente), required=True)  # Référence aux objets LigneVente
    acheteur = ReferenceField(Utilisateur, required=True)  # Référence à l'utilisateur

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'objet.
        """
        return (
            f"=== Vente ===\n"
            f"Acheteur: {self.acheteur}\n"
            f"Prix total: {self.prix_total:.2f} €\n"
            f"Numéro de vente: {self.numero_vente}\n"
            f"Date de vente: {self.date_vente}\n"
            f"Modalité: {self.modalite}\n"
            f"Lignes de vente: {len(self.lignes)} ligne(s)\n"
            "================="
        )

    def save(self, *args, **kwargs) -> None:
        """
        Sauvegarde la facture de vente dans la base de données MongoDB.
        """
        self.modalite = self.modalite  # Convertir l'énumération en sa valeur
        super().save(*args, **kwargs)  # Utilisation de la méthode `save()` de MongoEngine

    def delete(self, *args, **kwargs) -> None:
        """
        Supprime la facture de vente de la base de données MongoDB.
        """
        if self.numero_vente:
            super().delete(*args, **kwargs)  # Utilisation de la méthode `delete()` de MongoEngine
        else:
            raise ValueError("Impossible de supprimer une facture sans numéro de vente.")

    @classmethod
    def find_by_acheteur(cls, acheteur_id: str):
        """
        Recherche des factures par l'ID de l'acheteur dans MongoDB.
        """
        return cls.objects(acheteur=ObjectId(acheteur_id))

    @classmethod
    def find_by_numero(cls, numero_vente: str):
        """
        Recherche une facture par son numéro de vente.
        """
        return cls.objects(numero_vente=numero_vente).first()

    @classmethod
    def find_all(cls):
        """
        Recherche toutes les factures dans la base de données.
        """
        return cls.objects.all()

    def update(self, *args, **kwargs) -> None:
        """
        Met à jour la facture de vente dans la base de données MongoDB.
        """
        if self.numero_vente:
            data = {
                'prix_total': self.prix_total,
                'numero_vente': self.numero_vente,
                'date_vente': self.date_vente,
                'modalite': self.modalite,
                'lignes': self.lignes,
                'acheteur': self.acheteur
            }
            self.update(**data)
        else:
            raise ValueError("Impossible de mettre à jour une facture sans numéro de vente.")
