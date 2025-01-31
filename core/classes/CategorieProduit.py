from dependency_injector.wiring import inject, Provide
from core.dependency_injection.container import Container
from core.data.mongo_handler import MongoDBHandler
from bson import ObjectId  # Pour gérer les ObjectId de MongoDB

class CategorieProduit:
    @inject
    def __init__(self, 
                 libelle: str, 
                 description: str, 
                 mongo_handler: MongoDBHandler = Provide[Container.category_handler], 
                 id: str = None) -> None:
        self._id = id  # ID MongoDB
        self._libelle = libelle
        self._description = description
        self.mongo_handler = mongo_handler  # L'injection de dépendance

    @property
    def libelle(self) -> str:
        return self._libelle

    @libelle.setter
    def libelle(self, value: str) -> None:
        self._libelle = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @inject
    def save(self) -> None:
        """
        Sauvegarde la catégorie dans la base de données MongoDB.
        Si l'ID existe, il met à jour la catégorie. Sinon, il crée une nouvelle catégorie.
        """
        data = {
            'libelle': self._libelle,
            'description': self._description
        }
        if self._id:
            # Mise à jour de la catégorie existante
            self.mongo_handler.update({'_id': ObjectId(self._id)}, data)
        else:
            # Création d'une nouvelle catégorie
            result = self.mongo_handler.save(data)
            self._id = str(result.inserted_id)  # Stocke le nouvel ID
            
    @inject
    def delete(self) -> None:
        """
        Supprime la catégorie de la base de données MongoDB.
        """
        if self._id:
            self.mongo_handler.delete({'_id': ObjectId(self._id)})
            self._id = None  # Réinitialise l'ID après suppression
        else:
            raise ValueError("Impossible de supprimer une catégorie sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.category_handler]):
        """
        Recherche des catégories en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            Cursor: Un curseur MongoDB pour parcourir les documents trouvés.
        """
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.category_handler]):
        """
        Recherche une seule catégorie en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données de la catégorie trouvée, ou None si aucune catégorie n'est trouvée.
        """
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.category_handler]):
        """
        Recherche une catégorie par son ID MongoDB.

        Args:
            id (str): L'ID MongoDB de la catégorie à rechercher.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données de la catégorie trouvée, ou None si aucune catégorie n'est trouvée.
        """
        return mongo_handler.find_by_id(ObjectId(id))
