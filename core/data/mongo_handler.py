# core/database/mongo_handler.py
from core.data.connection import MongoDBConnection
from pymongo.errors import PyMongoError

class MongoDBHandler:
    """
    Une classe helper pour effectuer des opérations CRUD sur une collection MongoDB.
    Cette classe utilise la connexion singleton de `MongoDBConnection`.
    """

    def __init__(self, collection_name):
        """
        Initialise le handler avec une collection MongoDB spécifique.
        
        Args:
            collection_name (str): Le nom de la collection MongoDB à utiliser.
        
        Raises:
            PyMongoError: Si la connexion à MongoDB échoue ou si la collection n'est pas accessible.
        """
        try:
            # Utilise la connexion singleton
            self.connection = MongoDBConnection()
            # Récupère la base de données
            self.db = self.connection.get_db()
            # Sélectionne la collection
            self.collection = self.db[collection_name]
        except PyMongoError as e:
            raise PyMongoError(f"Erreur lors de l'initialisation du handler : {e}")

    def save(self, data):
        """
        Insère un document dans la collection MongoDB.
        
        Args:
            data (dict): Le document à insérer dans la collection.
        
        Raises:
            PyMongoError: Si l'insertion échoue.
        """
        try:
            self.collection.insert_one(data)
        except PyMongoError as e:
            raise PyMongoError(f"Erreur lors de l'insertion du document : {e}")
    
    def find(self, query):
        """
        Recherche des documents dans la collection MongoDB en fonction des critères spécifiés.
        
        Args:
            query (dict): Un dictionnaire de critères de recherche.
        
        Returns:
            Cursor: Un curseur MongoDB pour parcourir les documents trouvés.
        
        Raises:
            PyMongoError: Si la recherche échoue.
        """
        try:
            return self.collection.find(query)
        except PyMongoError as e:
            raise PyMongoError(f"Erreur lors de la recherche des documents : {e}")

    def find_by_id(self, id):
        """
        Recherche un document par son ID dans la collection MongoDB.
        
        Args:
            id: L'ID du document à rechercher.
        
        Returns:
            dict: Le document trouvé, ou None si aucun document n'est trouvé.
        
        Raises:
            PyMongoError: Si la recherche échoue.
        """
        try:
            return self.collection.find_one({'_id': id})
        except PyMongoError as e:
            raise PyMongoError(f"Erreur lors de la recherche du document : {e}")

    def update(self, query, update_data):
        """
        Met à jour un document dans la collection MongoDB.
        
        Args:
            query (dict): La requête pour trouver le document à mettre à jour.
            update_data (dict): Les nouvelles valeurs à appliquer au document.
        
        Raises:
            PyMongoError: Si la mise à jour échoue.
        """
        try:
            self.collection.update_one(query, {'$set': update_data})
        except PyMongoError as e:
            raise PyMongoError(f"Erreur lors de la mise à jour du document : {e}")

    def delete(self, query):
        """
        Supprime un document de la collection MongoDB.
        
        Args:
            query (dict): La requête pour trouver le document à supprimer.
        
        Raises:
            PyMongoError: Si la suppression échoue.
        """
        try:
            self.collection.delete_one(query)
        except PyMongoError as e:
            raise PyMongoError(f"Erreur lors de la suppression du document : {e}")