from typing import List
from core.enums.ModaliteVenteEnum import ModaliteVenteEnum
from LigneVente import LigneVente
from core.classes.Utilisateur import Utilisateur
from core.data.mongo_handler import MongoDBHandler
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from core.dependency_injection.container import Container
from bson import ObjectId  # Pour les ObjectId de MongoDB


class FactureVente:
    @inject
    def __init__(
            self,
            prix_total: float,
            numero_vente: datetime,
            date_vente: str,
            modalite: ModaliteVenteEnum,
            lignes: List[LigneVente],
            acheteur: Utilisateur,
            mongo_handler: MongoDBHandler = Provide[Container.facture_handler]  # Injection du handler MongoDB
    ) -> None:
        self._acheteur = acheteur
        self._prix_total = prix_total
        self._numero_vente = numero_vente
        self._date_vente = date_vente
        self._modalite = modalite
        self._lignes = lignes
        self.mongo_handler = mongo_handler  # Injection du handler MongoDB

    @property
    def acheteur(self) -> Utilisateur:
        return self._acheteur

    @property
    def prix_total(self) -> float:
        return self._prix_total

    @prix_total.setter
    def prix_total(self, value: float) -> None:
        self._prix_total = value

    @property
    def numero_vente(self) -> str:
        return self._numero_vente

    @numero_vente.setter
    def numero_vente(self, value: str) -> None:
        self._numero_vente = value

    @property
    def date_vente(self) -> datetime:
        return self._date_vente

    @date_vente.setter
    def date_vente(self, value: datetime) -> None:
        self._date_vente = value

    @property
    def modalite(self) -> ModaliteVenteEnum:
        return self._modalite

    @acheteur.setter
    def acheteur(self, value: Utilisateur) -> None:
        self._acheteur = value

    @modalite.setter
    def modalite(self, value: ModaliteVenteEnum) -> None:
        self._modalite = value

    @property
    def lignes(self) -> List[LigneVente]:
        return self._lignes

    @lignes.setter
    def lignes(self, value: List[LigneVente]) -> None:
        self._lignes = value

    def save(self) -> None:
        """
        Sauvegarde la facture de vente dans la base de données MongoDB.
        """
        data = {
            'prix_total': self._prix_total,
            'numero_vente': self._numero_vente,
            'date_vente': self._date_vente,
            'modalite': self._modalite.value,  # Enregistre la valeur de l'énumération
            'lignes': [ligne.to_dict() for ligne in self._lignes],  # Transformation des lignes en dictionnaires
            'acheteur_id': self._acheteur.id  # Lien vers l'acheteur par son ID
        }
        # Sauvegarde de la facture dans MongoDB via le handler
        self.mongo_handler.save(data)

    @inject
    def delete(self, mongo_handler: MongoDBHandler = Provide[Container.facture_handler]) -> None:
        """
        Supprime la facture de vente de la base de données MongoDB.
        """
        if self._numero_vente:
            mongo_handler.delete({'numero_vente': self._numero_vente})
        else:
            raise ValueError("Impossible de supprimer une facture sans numéro de vente.")

    @inject
    def find_by_acheteur(cls, acheteur_id: str, mongo_handler: MongoDBHandler = Provide[Container.facture_handler]):
        """
        Recherche des factures par l'ID de l'acheteur dans MongoDB.
        """
        return mongo_handler.find({'acheteur_id': acheteur_id})

    @inject
    def find_by_numero(cls, numero_vente: str, mongo_handler: MongoDBHandler = Provide[Container.facture_handler]):
        """
        Recherche une facture par son numéro de vente.
        """
        return mongo_handler.find({'numero_vente': numero_vente})

    @inject
    def find_all(cls, mongo_handler: MongoDBHandler = Provide[Container.facture_handler]):
        """
        Recherche toutes les factures dans la base de données.
        """
        return mongo_handler.find({})

    @inject
    def update(self, mongo_handler: MongoDBHandler = Provide[Container.facture_handler]) -> None:
        """
        Met à jour la facture de vente dans la base de données MongoDB.
        """
        data = {
            'prix_total': self._prix_total,
            'numero_vente': self._numero_vente,
            'date_vente': self._date_vente,
            'modalite': self._modalite.value,
            'lignes': [ligne.to_dict() for ligne in self._lignes],
            'acheteur_id': self._acheteur.id
        }
        if self._numero_vente:
            mongo_handler.update({'numero_vente': self._numero_vente}, data)
        else:
            raise ValueError("Impossible de mettre à jour une facture sans numéro de vente.")
