from dependency_injector.wiring import inject, Provide
from core.dependency_injection.container import Container
from core.data.mongo_handler import MongoDBHandler
from core.classes.Utilisateur import Utilisateur
from bson import ObjectId

from core.utils import PasswordUtils

class Admin(Utilisateur):
    @inject
    def __init__(
        self,
        nom: str,
        prenom: str,
        telephone: str,
        adresse: str,
        username: str,
        password: str,
        mongo_handler: MongoDBHandler = Provide[Container.admin_handler],
        id: str = None
    ) -> None:
        super().__init__(nom, prenom, telephone, adresse, username, password)
        self._id = id
        self.mongo_handler = mongo_handler

    @property
    def id(self) -> str:
        return self._id

    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, value: str) -> None:
        self._username = value
    
    @property
    def password(self) -> str:
        return self._password
    
    @password.setter
    def password(self, value: str) -> None:
        self._password = PasswordUtils.hash_password(value)

    def save(self) -> None:
        """
        Sauvegarde l'admin dans la base de données MongoDB.
        Si l'admin a un ID, il est mis à jour. Sinon, un nouvel admin est créé.
        """
        data = {
            'nom': self._nom,
            'prenom': self._prenom,
            'telephone': self._telephone,
            'adresse': self._adresse,
            'username': self._username,
            'password': self._password  # Supposant que le hash est déjà appliqué
        }
        if self._id:
            self.mongo_handler.update({'_id': ObjectId(self._id)}, data)
        else:
            result = self.mongo_handler.save(data)
            self._id = str(result.inserted_id)

    def delete(self) -> None:
        """
        Supprime l'admin de la base de données MongoDB.
        """
        if self._id:
            self.mongo_handler.delete({'_id': ObjectId(self._id)})
            self._id = None
        else:
            raise ValueError("Impossible de supprimer un admin sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.admin_handler]):
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.admin_handler]):
        return mongo_handler.find_one(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.admin_handler]):
        return mongo_handler.find_by_id(ObjectId(id))
