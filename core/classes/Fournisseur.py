from dependency_injector.wiring import inject, Provide
from core.dependency_injection.container import Container
from core.data.mongo_handler import MongoDBHandler
from bson import ObjectId

class Fournisseur:
    @inject
    def __init__(
        self, 
        nom: str, 
        adresse: str, 
        telephone: str, 
        email: str, 
        mongo_handler: MongoDBHandler = Provide[Container.fournisseur_handler],
        id: str = None
    ) -> None:
        self._id = id
        self._nom = nom
        self._adresse = adresse
        self._telephone = telephone
        self._email = email
        self.mongo_handler = mongo_handler

    @property
    def id(self) -> str:
        return self._id

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, value: str) -> None:
        self._nom = value

    @property
    def adresse(self) -> str:
        return self._adresse

    @adresse.setter
    def adresse(self, value: str) -> None:
        self._adresse = value

    @property
    def telephone(self) -> str:
        return self._telephone

    @telephone.setter
    def telephone(self, value: str) -> None:
        self._telephone = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    @inject
    def save(self) -> None:
        data = {
            'nom': self._nom,
            'adresse': self._adresse,
            'telephone': self._telephone,
            'email': self._email
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
            raise ValueError("Impossible de supprimer un fournisseur sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.fournisseur_handler]):
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.fournisseur_handler]):
        return mongo_handler.find_one(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.fournisseur_handler]):
        return mongo_handler.find_by_id(ObjectId(id))
