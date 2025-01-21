class LigneVente:
    def __init__(self, quantite: int, prix_total_ligne: float) -> None:
        self._quantite = quantite
        self._prix_total_ligne = prix_total_ligne

    @property
    def quantite(self) -> int:
        return self._quantite

    @quantite.setter
    def quantite(self, value: int) -> None:
        self._quantite = value

    @property
    def prix_total_ligne(self) -> float:
        return self._prix_total_ligne

    @prix_total_ligne.setter
    def prix_total_ligne(self, value: float) -> None:
        self._prix_total_ligne = value
