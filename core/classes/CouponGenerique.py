from datetime import date
from typing import List, Optional
from Produit import Produit
from dependency_injector.wiring import inject, Provide
from core.dependency_injection.container import Container
from core.data.mongo_handler import MongoDBHandler
from bson import ObjectId

class CouponGenerique:
    @inject
    def __init__(self, 
                 actif: bool, 
                 cumulable: bool, 
                 date_expiration: date, 
                 reduction_montant: float, 
                 reduction_taux: float, 
                 global_coupon: bool, 
                 produits: Optional[List[Produit]] = None,
                 mongo_handler: MongoDBHandler = Provide[Container.coupon_handler]) -> None:
        """
        Initialise un coupon générique avec les informations de base et l'injection de dépendances pour MongoDB.

        Args:
            actif (bool): Indique si le coupon est actif.
            cumulable (bool): Indique si le coupon est cumulable avec d'autres.
            date_expiration (date): Date d'expiration du coupon.
            reduction_montant (float): Montant de réduction fixe.
            reduction_taux (float): Taux de réduction en pourcentage.
            global_coupon (bool): Indique si le coupon est global.
            produits (Optional[List[Produit]]): Liste des produits auxquels le coupon s'applique (optionnel).
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.
        """
        self._actif = actif
        self._cumulable = cumulable
        self._date_expiration = date_expiration
        self._reduction_montant = reduction_montant
        self._reduction_taux = reduction_taux
        self._global_coupon = global_coupon
        self._produits = produits if produits is not None else []
        self.mongo_handler = mongo_handler
        self._id = None  # ID MongoDB, à attribuer lors de l'enregistrement.

    @property
    def actif(self) -> bool:
        return self._actif

    @actif.setter
    def actif(self, value: bool) -> None:
        self._actif = value

    @property
    def cumulable(self) -> bool:
        return self._cumulable

    @cumulable.setter
    def cumulable(self, value: bool) -> None:
        self._cumulable = value

    @property
    def date_expiration(self) -> date:
        return self._date_expiration

    @date_expiration.setter
    def date_expiration(self, value: date) -> None:
        self._date_expiration = value

    @property
    def reduction_montant(self) -> float:
        return self._reduction_montant

    @reduction_montant.setter
    def reduction_montant(self, value: float) -> None:
        self._reduction_montant = value

    @property
    def reduction_taux(self) -> float:
        return self._reduction_taux

    @reduction_taux.setter
    def reduction_taux(self, value: float) -> None:
        self._reduction_taux = value

    @property
    def global_coupon(self) -> bool:
        return self._global_coupon

    @global_coupon.setter
    def global_coupon(self, value: bool) -> None:
        self._global_coupon = value

    @property
    def produits(self) -> List[Produit]:
        return self._produits

    @produits.setter
    def produits(self, value: List[Produit]) -> None:
        if self._global_coupon:
            raise ValueError("Un coupon global ne peut pas avoir de produits spécifiques.")
        self._produits = value

    def ajouter_produit(self, produit: Produit) -> None:
        if self._global_coupon:
            raise ValueError("Un coupon global ne peut pas être lié à des produits spécifiques.")
        self._produits.append(produit)

    def retirer_produit(self, produit: Produit) -> None:
        if produit in self._produits:
            self._produits.remove(produit)

    def est_valide_pour_produit(self, produit: Produit) -> bool:
        return self._global_coupon or produit in self._produits
    
    @inject
    def save(self) -> None:
        """
        Sauvegarde le coupon générique dans la base de données MongoDB.
        """
        data = {
            'actif': self._actif,
            'cumulable': self._cumulable,
            'date_expiration': self._date_expiration,
            'reduction_montant': self._reduction_montant,
            'reduction_taux': self._reduction_taux,
            'global_coupon': self._global_coupon,
            'produits': [produit.id for produit in self._produits]  # Enregistre les ID des produits
        }
        result = self.mongo_handler.save(data)
        self._id = str(result.inserted_id)  # Stocke l'ID du coupon créé
        
    @inject
    def delete(self) -> None:
        """
        Supprime le coupon générique de la base de données MongoDB.
        """
        if self._id:
            self.mongo_handler.delete({'_id': ObjectId(self._id)})
            self._id = None  # Réinitialise l'ID après suppression
        else:
            raise ValueError("Impossible de supprimer un coupon sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.coupon_handler]):
        """
        Recherche des coupons génériques en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            Cursor: Un curseur MongoDB pour parcourir les documents trouvés.
        """
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.coupon_handler]):
        """
        Recherche un seul coupon générique en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données du coupon trouvé, ou None si aucun coupon n'est trouvé.
        """
        return mongo_handler.find_one(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.coupon_handler]):
        """
        Recherche un coupon générique par son ID MongoDB.

        Args:
            id (str): L'ID MongoDB du coupon générique à rechercher.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données du coupon trouvé, ou None si aucun coupon n'est trouvé.
        """
        return mongo_handler.find_by_id(ObjectId(id))
