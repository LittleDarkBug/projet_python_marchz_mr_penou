# core/database/connection.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

class MongoDBConnection:
    """
    Une classe singleton pour gérer la connexion à MongoDB.
    Cette classe garantit qu'une seule instance de connexion est utilisée dans toute l'application.
    """

    _instance = None  # Stocke l'instance unique de la connexion
    db = None  # Stocke l'objet de base de données MongoDB
    client = None  # Stocke l'objet client MongoDB

    def __new__(cls, *args, **kwargs):
        """
        Surcharge de la méthode __new__ pour implémenter le pattern singleton.
        Si une instance existe déjà, elle est retournée. Sinon, une nouvelle instance est créée.
        """
        if not cls._instance:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance.initialize_connection(*args, **kwargs)
        return cls._instance

    def initialize_connection(self, host='localhost', port=27017, database_name='mrplenou', username='admin', password='admin'):
        """
        Initialise la connexion à MongoDB.
        
        Args:
            host (str): L'hôte de la base de données MongoDB (par défaut : 'localhost').
            port (int): Le port de la base de données MongoDB (par défaut : 27017).
            database_name (str): Le nom de la base de données à utiliser (par défaut : 'local')
            username (str): Le nom d'utilisateur 
            password (str): Le mot de passe

        
        Raises:
            ConnectionFailure: Si la connexion à MongoDB échoue.
        """
        try:
            self.client = MongoClient(host, port , username=username, password=password)
            self.db = self.client[database_name]  # Sélectionne la base de données
            #print(self.client.list_database_names())
            # Vérifie si la connexion est active
            self.client.admin.command('ping')
        except ConnectionFailure as e:
            raise ConnectionFailure(f"Échec de la connexion à MongoDB : {e}")

    def get_db(self):
        """
        Retourne l'objet de base de données MongoDB.
        
        Returns:
            Database: L'objet de base de données MongoDB.
        
        Raises:
            PyMongoError: Si la base de données n'est pas accessible.
        """
        if self.db == None:
            raise PyMongoError("La base de données n'est pas initialisée.")
        return self.db

    def close_connection(self):
        """
        Ferme la connexion à MongoDB.
        Cette méthode peut être utilisée pour libérer les ressources lorsque la connexion n'est plus nécessaire.
        """
        if self.client:
            self.client.close()  # Ferme la connexion
            self.client = None   # Réinitialise le client
            self.db = None       # Réinitialise la base de données