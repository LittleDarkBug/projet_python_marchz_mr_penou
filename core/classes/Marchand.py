from core.classes.Utilisateur import Utilisateur
from core.enums.TypeMarchandEnum import TypeMarchandEnum
from dependency_injector.wiring import inject, Provide
from core.dependency_injection.container import Container
from core.data.mongo_handler import MongoDBHandler
from bson import ObjectId
from core.utils.PasswordUtils import PasswordUtils

class Marchand(Utilisateur):
    @inject
    def __init__(
        self, 
        nom: str, 
        prenom: str, 
        telephone: str, 
        adresse: str, 
        username: str,
        password: str,
        description: str, 
        type_marchand: TypeMarchandEnum, 
        mongo_handler: MongoDBHandler = Provide[Container.marchand_handler],
        id: str = None
    ) -> None:
        super().__init__(nom, prenom, telephone, adresse, description ,username, password)
        self._type_marchand = type_marchand
        self._x = None
        self._y = None
        self._id = id
        self.mongo_handler = mongo_handler

    @property
    def id(self) -> str:
        return self._id

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

    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, value: str) -> None:
        self._username = value
    
    @property
    def password(self) -> bytes or str:
        return self._password
    
    @password.setter
    def password(self, value: str) -> None:
        self._password = PasswordUtils.hash_password(value)

    @inject
    def save(self) -> None:
        data = {
            'nom': self.nom,
            'prenom': self.prenom,
            'telephone': self.telephone,
            'adresse': self.adresse,
            'description': self.description,
            'type_marchand': self._type_marchand.value,
            'password': self.password,
            'username': self.username,
            'x': self._x,
            'y': self._y
        }
        if self._id:
            self.mongo_handler.update({'_id': ObjectId(self._id)}, data)
        else:
            result = self.mongo_handler.save(data)
            self._id = str(result.inserted_id)
            
    @inject
    def delete(self) -> None:
        if self._id:
            self.mongo_handler.delete({'_id': ObjectId(self._id)})
            self._id = None
        else:
            raise ValueError("Impossible de supprimer un marchand sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.marchand_handler]):
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.marchand_handler]):
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.marchand_handler]):
        return mongo_handler.find_by_id(ObjectId(id))
