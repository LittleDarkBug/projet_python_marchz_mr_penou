from core.classes.Utilisateur import Utilisateur
from core.data.connection import initialize_connection
from pymongo.errors import PyMongoError
from core.utils.PasswordUtils import PasswordUtils

class AuthManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    
    def authenticate_user(self, username: str, password: str) -> bool:
        initialize_connection()
        user = Utilisateur.objects(username=username).first()
        if not user:
            return False  # Utilisateur non trouvé
        
        stored_hash = user.password
        return PasswordUtils.verify_password(password, stored_hash)