from typing import List
from core.enums.ModaliteVenteEnum import ModaliteVenteEnum
from LigneVente import LigneVente
from core.classes.Utilisateur import Utilisateur
from datetime import datetime

class FactureVente:
    def __init__(self, prix_total: float, numero_vente: datetime, date_vente: str, modalite: ModaliteVenteEnum, lignes: List[LigneVente], acheteur: Utilisateur) -> None:
        self._acheteur = acheteur
        self._prix_total = prix_total
        self._numero_vente = numero_vente
        self._date_vente = date_vente
        self._modalite = modalite
        self._lignes = lignes

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
