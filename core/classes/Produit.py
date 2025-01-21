from typing import List
from core.enums.TypeUniteEnum import TypeUniteEnum
from CouponGenerique import CouponGenerique
from Fournisseur import Fournisseur

class Produit:
    def __init__(self, libelle: str, prix_achat: float, prix_vente: float, description: str, type_unite: TypeUniteEnum, quantite: int, fournisseur: Fournisseur) -> None:
        self._libelle = libelle
        self._prix_achat = prix_achat
        self._prix_vente = prix_vente
        self._description = description
        self._type_unite = type_unite
        self._quantite = quantite
        self._fournisseur = fournisseur
        self._coupons: List[CouponGenerique] = []

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
        if coupon not in self._coupons:
            self._coupons.append(coupon)
            if self not in coupon.produits:
                coupon.ajouter_produit(self)

    def retirer_coupon(self, coupon: CouponGenerique) -> None:
        if coupon in self._coupons:
            self._coupons.remove(coupon)
            if self in coupon.produits:
                coupon.retirer_produit(self)
