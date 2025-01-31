from typing import List, Tuple
from core.dependency_injection.container import Container
from core.data.mongo_handler import MongoDBHandler
from bson import ObjectId
from dependency_injector.wiring import inject, Provide
from core.classes.Marchand import Marchand

class EspaceMarche:
    @inject
    def __init__(self,
                 nom: str,
                 taille: Tuple[int, int],
                 mongo_handler: MongoDBHandler = Provide[Container.marche_handler],
                 id: str = None) -> None:
        """
        Initialise un nouvel espace de marché ou charge un espace existant.

        Args:
            nom (str): Le nom de l'espace de marché.
            taille (Tuple[int, int]): Les dimensions de l'espace (largeur, hauteur).
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.
            id (str): L'ID MongoDB de l'espace de marché (optionnel, pour un espace existant).
        """
        self._id = id  # ID MongoDB
        self._nom = nom
        self._taille = taille
        self._marchands = []
        self._mongo_handler = mongo_handler

    @property
    def id(self) -> str:
        """Retourne l'ID MongoDB de l'espace de marché."""
        return self._id

    @property
    def nom(self) -> str:
        """Retourne le nom de l'espace de marché."""
        return self._nom

    @nom.setter
    def nom(self, value: str) -> None:
        """Modifie le nom de l'espace de marché."""
        self._nom = value

    @property
    def taille(self) -> Tuple[int, int]:
        """Retourne les dimensions de l'espace de marché."""
        return self._taille

    @taille.setter
    def taille(self, value: Tuple[int, int]) -> None:
        """Modifie la taille de l'espace de marché."""
        self._taille = value

    @property
    def marchands(self) -> List[Marchand]:
        """Retourne la liste des marchands dans l'espace de marché."""
        return self._marchands

    @marchands.setter
    def marchands(self, value: List[Marchand]) -> None:
        """Modifie la liste des marchands dans l'espace de marché."""
        self._marchands = value

    def est_position_libre(self, x: int, y: int) -> bool:
        """
        Vérifie si la position (x, y) est libre dans l'espace de marché.

        Args:
            x (int): La coordonnée x de la position.
            y (int): La coordonnée y de la position.

        Returns:
            bool: True si la position est libre, False sinon.
        """
        return all(marchand.x != x or marchand.y != y for marchand in self._marchands)

    def ajouter_marchand(self, marchand: Marchand, x: int, y: int) -> None:
        """
        Ajoute un marchand à une position libre dans l'espace de marché en lui assignant une position (x, y).

        Args:
            marchand (Marchand): Le marchand à ajouter.
            x (int): La coordonnée x de la position.
            y (int): La coordonnée y de la position.

        Raises:
            ValueError: Si la position est déjà occupée.
        """
        if self.est_position_libre(x, y):
            marchand.x = x  # Assigner la position x au marchand
            marchand.y = y  # Assigner la position y au marchand
            self._marchands.append(marchand)  # Ajouter le marchand au marché
        else:
            raise ValueError(f"La position ({x}, {y}) est déjà occupée.")

    def obtenir_emplacements_libres(self) -> List[Tuple[int, int]]:
        """
        Retourne une liste d'emplacements libres dans l'espace de marché.

        Returns:
            List[Tuple[int, int]]: Liste des coordonnées (x, y) des emplacements libres.
        """
        emplacements_libres = []
        for x in range(self._taille[0]):  # Parcourt les x possibles
            for y in range(self._taille[1]):  # Parcourt les y possibles
                if self.est_position_libre(x, y):
                    emplacements_libres.append((x, y))  # Ajoute la position libre
        return emplacements_libres
    
    @inject
    def save(self) -> None:
        """
        Sauvegarde l'espace de marché dans la base de données MongoDB.
        Si l'espace de marché a un ID, il est mis à jour. Sinon, un nouvel espace est créé.
        """
        data = {
            'nom': self._nom,
            'taille': self._taille,
            'marchands': [marchand.to_dict() for marchand in self._marchands]  # Assumer que Marchand a une méthode to_dict
        }
        if self._id:
            # Met à jour l'espace de marché existant
            self._mongo_handler.update({'_id': ObjectId(self._id)}, data)
        else:
            # Crée un nouvel espace de marché
            result = self._mongo_handler.save(data)
            self._id = str(result.inserted_id)  # Stocke le nouvel ID
            
    @inject
    def delete(self) -> None:
        """
        Supprime l'espace de marché de la base de données MongoDB.
        """
        if self._id:
            self._mongo_handler.delete({'_id': ObjectId(self._id)})
            self._id = None  # Réinitialise l'ID après suppression
        else:
            raise ValueError("Impossible de supprimer un espace de marché sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.marche_handler]):
        """
        Recherche des espaces de marché en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            Cursor: Un curseur MongoDB pour parcourir les documents trouvés.
        """
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.marche_handler]):
        """
        Recherche un seul espace de marché en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données de l'espace de marché trouvé, ou None si aucun espace de marché n'est trouvé.
        """
        return mongo_handler.find_one(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.marche_handler]):
        """
        Recherche un espace de marché par son ID MongoDB.

        Args:
            id (str): L'ID MongoDB de l'espace de marché à rechercher.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données de l'espace de marché trouvé, ou None si aucun espace de marché n'est trouvé.
        """
        return mongo_handler.find_by_id(ObjectId(id))
