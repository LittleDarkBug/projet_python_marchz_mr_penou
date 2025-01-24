# core/classes/produit.py
from typing import List
from dependency_injector.wiring import inject, Provide
from core.dependency_injection.container import Container
from core.data.mongo_handler import MongoDBHandler
from core.enums.TypeUniteEnum import TypeUniteEnum
from core.classes.CouponGenerique import CouponGenerique
from core.classes.Fournisseur import Fournisseur
from bson import ObjectId

class Produit:
    @inject
    def __init__(
        self,
        libelle: str,
        prix_achat: float,
        prix_vente: float,
        description: str,
        type_unite: TypeUniteEnum,
        quantite: int,
        fournisseur: Fournisseur,
        mongo_handler: MongoDBHandler = Provide[Container.produit_handler],
        id: str = None  # Ajout d'un ID pour les produits existants
    ) -> None:
        """
        Initialise un nouveau produit ou charge un produit existant.

        Args:
            libelle (str): Le libellé du produit.
            prix_achat (float): Le prix d'achat du produit.
            prix_vente (float): Le prix de vente du produit.
            description (str): Une description du produit.
            type_unite (TypeUniteEnum): Le type d'unité du produit.
            quantite (int): La quantité disponible du produit.
            fournisseur (Fournisseur): Le fournisseur du produit.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.
            id (str): L'ID MongoDB du produit (optionnel, pour les produits existants).
        """
        self._id = id  # ID MongoDB
        self._libelle = libelle
        self._prix_achat = prix_achat
        self._prix_vente = prix_vente
        self._description = description
        self._type_unite = type_unite
        self._quantite = quantite
        self._fournisseur = fournisseur
        self._coupons: List[CouponGenerique] = []
        self.mongo_handler = mongo_handler

    @property
    def id(self) -> str:
        """Retourne l'ID MongoDB du produit."""
        return self._id

    @property
    def libelle(self) -> str:
        return self._libelle

    @libelle.setter
    def libelle(self, value: str) -> None:
        self._libelle = value

    @property
    def prix_achat(self) -> float:
        return self._prix_achat

    @prix_achat.setter
    def prix_achat(self, value: float) -> None:
        self._prix_achat = value

    @property
    def prix_vente(self) -> float:
        return self._prix_vente

    @prix_vente.setter
    def prix_vente(self, value: float) -> None:
        self._prix_vente = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def type_unite(self) -> TypeUniteEnum:
        return self._type_unite

    @type_unite.setter
    def type_unite(self, value: TypeUniteEnum) -> None:
        self._type_unite = value

    @property
    def quantite(self) -> int:
        return self._quantite

    @quantite.setter
    def quantite(self, value: int) -> None:
        self._quantite = value

    @property
    def fournisseur(self) -> Fournisseur:
        return self._fournisseur

    @fournisseur.setter
    def fournisseur(self, value: Fournisseur) -> None:
        self._fournisseur = value

    @property
    def coupons(self) -> List[CouponGenerique]:
        return self._coupons

    def ajouter_coupon(self, coupon: CouponGenerique) -> None:
        """
        Ajoute un coupon au produit et met à jour la relation bidirectionnelle.

        Args:
            coupon (CouponGenerique): Le coupon à ajouter.
        """
        if coupon not in self._coupons:
            self._coupons.append(coupon)
            if self not in coupon.produits:
                coupon.ajouter_produit(self)

    def retirer_coupon(self, coupon: CouponGenerique) -> None:
        """
        Retire un coupon du produit et met à jour la relation bidirectionnelle.

        Args:
            coupon (CouponGenerique): Le coupon à retirer.
        """
        if coupon in self._coupons:
            self._coupons.remove(coupon)
            if self in coupon.produits:
                coupon.retirer_produit(self)

    def save(self) -> None:
        """
        Sauvegarde le produit dans la base de données MongoDB.
        Si le produit a un ID, il est mis à jour. Sinon, un nouveau produit est créé.
        """
        data = {
            'libelle': self._libelle,
            'prix_achat': self._prix_achat,
            'prix_vente': self._prix_vente,
            'description': self._description,
            'type_unite': self._type_unite.value,  # Convertit l'enum en valeur
            'quantite': self._quantite,
            'fournisseur': self._fournisseur.to_dict(),  # Stocke l'objet Fournisseur entier
            'coupons': [coupon.to_dict() for coupon in self._coupons]  # Stocke les objets CouponGenerique entiers
        }
        if self._id:
            # Met à jour le produit existant
            self.mongo_handler.update({'_id': ObjectId(self._id)}, data)
        else:
            # Crée un nouveau produit
            result = self.mongo_handler.save(data)
            self._id = str(result.inserted_id)  # Stocke le nouvel ID

    def delete(self) -> None:
        """
        Supprime le produit de la base de données MongoDB.
        """
        if self._id:
            self.mongo_handler.delete({'_id': ObjectId(self._id)})
            self._id = None  # Réinitialise l'ID après suppression
        else:
            raise ValueError("Impossible de supprimer un produit sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.products_handler]):
        """
        Recherche des produits en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            Cursor: Un curseur MongoDB pour parcourir les documents trouvés.
        """
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.products_handler]):
        """
        Recherche un seul produit en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données du produit trouvé, ou None si aucun produit n'est trouvé.
        """
        return mongo_handler.find_one(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.products_handler]):
        """
        Recherche un produit par son ID MongoDB.

        Args:
            id (str): L'ID MongoDB du produit à rechercher.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données du produit trouvé, ou None si aucun produit n'est trouvé.
        """
        return mongo_handler.find_by_id(ObjectId(id))