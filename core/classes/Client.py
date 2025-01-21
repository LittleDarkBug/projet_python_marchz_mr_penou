from core.classes.Utilisateur import Utilisateur
from core.classes.FactureVente import FactureVente
from typing import List

class Client(Utilisateur):
    def __init__(self, nom: str, prenom: str, telephone: str, adresse: str, description: str) -> None:
        super().__init__(nom, prenom, telephone, adresse, description)
        self._liste_achats[FactureVente] = []

    @property
    def liste_achats(self) -> List[FactureVente]:
        return self._liste_achats
    
    @liste_achats.setter
    def liste_achats(self, value: List[FactureVente]) -> None:
        self._liste_achats = value  