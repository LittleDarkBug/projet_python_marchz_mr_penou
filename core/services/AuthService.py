from core.data.connection import MongoDBConnection
from pymongo.errors import PyMongoError
from core.utils.PasswordUtils import PasswordUtils

class AuthManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        collection_name = 'users'
        try:
            self.connection = MongoDBConnection()
            if self.connection.db is None:
                self.connection.initialize_connection()
            self.db = self.connection.get_db()
            self.collection = self.db[collection_name]
        except PyMongoError as e:
            raise PyMongoError("Erreur lors de l'initialisation")
    
    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.collection.find_one({'username': username})
        if not user:
            return False  # Utilisateur non trouvé
        
        stored_hash = user['password']
        return PasswordUtils.verify_password(password, stored_hash)