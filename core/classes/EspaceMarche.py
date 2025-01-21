from core.classes.Marchand import Marchand
from typing import List, Tuple

class EspaceMarche:
    def __init__(self, nom: str, taille: Tuple[int, int]) -> None:
        self._nom = nom
        self._taille = taille
        self._marchands = []

    @property
    def nom(self) -> str:
        return self._nom
    
    @nom.setter
    def nom(self, value: str) -> None:
        self._nom = value
    
    @property
    def taille(self) -> Tuple[int, int]:
        return self._taille
    
    @taille.setter
    def taille(self, value: Tuple[int, int]) -> None:
        self._taille = value
    
    @property
    def marchands(self) -> List[Marchand]:
        return self._marchands
    
    @marchands.setter
    def marchands(self, value: List[Marchand]) -> None:
        self._marchands = value

    def est_position_libre(self, x: int, y: int) -> bool:
        """Vérifie si la position (x, y) est libre dans le marché."""
        for marchand in self._marchands:
            if marchand.x == x and marchand.y == y:
                return False  # La position est déjà occupée
        return True  # La position est libre

    def ajouter_marchand(self, marchand: Marchand, x: int, y: int) -> None:
        """Ajoute un marchand à une position libre dans le marché en lui assignant une position (x, y)."""
        if self.est_position_libre(x, y):
            marchand.x = x  # Assigner la position x au marchand
            marchand.y = y  # Assigner la position y au marchand
            self._marchands.append(marchand)  # Ajouter le marchand au marché
        else:
            print(f"La position ({x}, {y}) est déjà occupée.")

    def obtenir_emplacements_libres(self) -> List[Tuple[int, int]]:
        """Retourne une liste d'emplacements libres dans le marché."""
        emplacements_libres = []
        for x in range(self._taille[0]):  # Parcourt les x possibles
            for y in range(self._taille[1]):  # Parcourt les y possibles
                if self.est_position_libre(x, y):
                    emplacements_libres.append((x, y))  # Ajoute la position libre
        return emplacements_libres
