from datetime import date
from typing import List, Optional
from Produit import Produit

class CouponGenerique:
    def __init__(self, actif: bool, cumulable: bool, date_expiration: date, reduction_montant: float, reduction_taux: float, global_coupon: bool, produits: Optional[List[Produit]] = None) -> None:
        self._actif = actif
        self._cumulable = cumulable
        self._date_expiration = date_expiration
        self._reduction_montant = reduction_montant
        self._reduction_taux = reduction_taux
        self._global_coupon = global_coupon
        self._produits = produits if produits is not None else []

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
