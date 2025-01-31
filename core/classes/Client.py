from core.classes.Utilisateur import Utilisateur
from core.classes.FactureVente import FactureVente
from typing import List
from dependency_injector.wiring import inject, Provide
from core.dependency_injection.container import Container
from core.data.mongo_handler import MongoDBHandler
from core.utils.PasswordUtils import PasswordUtils

class Client(Utilisateur):
    @inject
    def __init__(self, 
                 nom: str, 
                 prenom: str, 
                 telephone: str, 
                 adresse: str, 
                 description: str, 
                 mongo_handler: MongoDBHandler = Provide[Container.client_handler]) -> None:
        super().__init__(nom, prenom, telephone, adresse, description, mongo_handler)
        self._liste_achats: List[FactureVente] = [] 
        self.mongo_handler = mongo_handler 

    @property
    def liste_achats(self) -> List[FactureVente]:
        return self._liste_achats

    @liste_achats.setter
    def liste_achats(self, value: List[FactureVente]) -> None:
        self._liste_achats = value
    
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

    def add_achat(self, facture: FactureVente) -> None:
        """
        Ajoute une facture à la liste des achats du client.
        """
        self._liste_achats.append(facture)

    def remove_achat(self, facture: FactureVente) -> None:
        """
        Retire une facture de la liste des achats du client.
        """
        if facture in self._liste_achats:
            self._liste_achats.remove(facture)
        else:
            raise ValueError("Cette facture n'est pas présente dans la liste des achats.")

    @inject
    def save(self) -> None:
        """
        Sauvegarde le client dans la base de données MongoDB.
        """
        data = {
            'nom': self.nom,
            'prenom': self.prenom,
            'telephone': self.telephone,
            'adresse': self.adresse,
            'description': self.description,
            'liste_achats': [facture.to_dict() for facture in self._liste_achats]  # Conversion des factures en dictionnaires
        }
        if self.id:
            # Mise à jour du client existant
            self.mongo_handler.update({'_id': self.id}, data)
        else:
            # Création d'un nouveau client
            result = self.mongo_handler.save(data)
            self._id = str(result.inserted_id)  # Stocke le nouvel ID
            
    @inject
    def delete(self) -> None:
        """
        Supprime le client de la base de données MongoDB.
        """
        if self.id:
            self.mongo_handler.delete({'_id': self.id})
            self._id = None  # Réinitialise l'ID après suppression
        else:
            raise ValueError("Impossible de supprimer un client sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.client_handler]):
        """
        Recherche des clients en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            Cursor: Un curseur MongoDB pour parcourir les documents trouvés.
        """
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.client_handler]):
        """
        Recherche un seul client en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données du client trouvé, ou None si aucun client n'est trouvé.
        """
        return mongo_handler.find_one(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.client_handler]):
        """
        Recherche un client par son ID MongoDB.

        Args:
            id (str): L'ID MongoDB du client à rechercher.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données du client trouvé, ou None si aucun client n'est trouvé.
        """
        return mongo_handler.find_by_id(id)
