from core.utils.PasswordUtils import PasswordUtils
from dependency_injector.wiring import inject, Provide
from core.dependency_injection.container import Container
from core.data.mongo_handler import MongoDBHandler
from bson import ObjectId  # Pour gérer les ObjectId de MongoDB

class Utilisateur:
    @inject
    def __init__(
        self,
        nom: str,
        prenom: str,
        telephone: str,
        adresse: str,
        description: str,
        username: str,
        password: str,
        mongo_handler: MongoDBHandler = Provide[Container.user_handler],
        id: str = None  # Ajout d'un ID pour les utilisateurs existants
    ) -> None:
        """
        Initialise un nouvel utilisateur ou charge un utilisateur existant.

        Args:
            nom (str): Le nom de l'utilisateur.
            prenom (str): Le prénom de l'utilisateur.
            telephone (str): Le numéro de téléphone de l'utilisateur.
            username (str) : Le pseudo d'utilisateur.
            password (str) : mot de passe utilisateur.
            adresse (str): L'adresse de l'utilisateur.
            description (str): Une description de l'utilisateur.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.
            id (str): L'ID MongoDB de l'utilisateur (optionnel, pour les utilisateurs existants).
        """
        self._id = id  # ID MongoDB
        self._nom = nom
        self._prenom = prenom
        self._telephone = telephone
        self._username = username
        self._password = PasswordUtils.hash_password(password)
        self._adresse = adresse
        self._description = description
        self.mongo_handler = mongo_handler

    @property
    def id(self) -> str:
        """Retourne l'ID MongoDB de l'utilisateur."""
        return self._id

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, value: str) -> None:
        self._nom = value

    @property
    def prenom(self) -> str:
        return self._prenom

    @prenom.setter
    def prenom(self, value: str) -> None:
        self._prenom = value
    
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

    @property
    def telephone(self) -> str:
        return self._telephone

    @telephone.setter
    def telephone(self, value: str) -> None:
        self._telephone = value

    @property
    def adresse(self) -> str:
        return self._adresse

    @adresse.setter
    def adresse(self, value: str) -> None:
        self._adresse = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    def save(self) -> None:
        """
        Sauvegarde l'utilisateur dans la base de données MongoDB.
        Si l'utilisateur a un ID, il est mis à jour. Sinon, un nouvel utilisateur est créé.
        """
        data = {
            'nom': self._nom,
            'prenom': self._prenom,
            'telephone': self._telephone,
            'adresse': self._adresse,
            'description': self._description,
            'password': self._password,
            'username': self._username
        }
        if self._id:
            # Met à jour l'utilisateur existant
            self.mongo_handler.update({'_id': ObjectId(self._id)}, data)
        else:
            # Crée un nouvel utilisateur
            result = self.mongo_handler.save(data)
            self._id = str(result.inserted_id)  # Stocke le nouvel ID

    def delete(self) -> None:
        """
        Supprime l'utilisateur de la base de données MongoDB.
        """
        if self._id:
            self.mongo_handler.delete({'_id': ObjectId(self._id)})
            self._id = None  # Réinitialise l'ID après suppression
        else:
            raise ValueError("Impossible de supprimer un utilisateur sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.user_handler]):
        """
        Recherche des utilisateurs en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            Cursor: Un curseur MongoDB pour parcourir les documents trouvés.
        """
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.user_handler]):
        """
        Recherche un seul utilisateur en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données de l'utilisateur trouvé, ou None si aucun utilisateur n'est trouvé.
        """
        return mongo_handler.find_one(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.user_handler]):
        """
        Recherche un utilisateur par son ID MongoDB.

        Args:
            id (str): L'ID MongoDB de l'utilisateur à rechercher.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données de l'utilisateur trouvé, ou None si aucun utilisateur n'est trouvé.
        """
        return mongo_handler.find_by_id(ObjectId(id))