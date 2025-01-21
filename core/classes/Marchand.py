from core.classes.Utilisateur import Utilisateur
from core.enums.TypeMarchandEnum import TypeMarchandEnum

class Marchand(Utilisateur):
    def __init__(self, nom: str, prenom: str, telephone: str, adresse: str, description: str, type_marchand: TypeMarchandEnum) -> None:
        super().__init__(nom, prenom, telephone, adresse, description)
        self._type_marchand = type_marchand
        self._x = None
        self._y = None

    @property
    def type_marchand(self) -> TypeMarchandEnum:
        return self._type_marchand

    @type_marchand.setter
    def type_marchand(self, value: TypeMarchandEnum) -> None:
        self._type_marchand = value

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, value: int) -> None:
        self._y = value
