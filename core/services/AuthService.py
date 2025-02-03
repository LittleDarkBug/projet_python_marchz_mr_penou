from core.classes.Client import Client
from core.classes.Marchand import Marchand
from core.classes.Utilisateur import Utilisateur
from core.data.connection import initialize_connection
from pymongo.errors import PyMongoError
from core.utils.PasswordUtils import PasswordUtils

class AuthManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthManager, cls).__new__(cls)
        return cls._instance
    
    def authenticate_user(self, username: str, password: str):
        """Authentifie l'utilisateur et retourne l'objet utilisateur spécifique (Marchand, Client, etc.)."""
        initialize_connection()
        user = Utilisateur.objects(username=username).first()  # Recherche de l'utilisateur générique
        if not user:
            return None  # Utilisateur non trouvé
        
        stored_hash = user.password
        if PasswordUtils.verify_password(password, stored_hash):  # Vérification du mot de passe
            # Si le mot de passe est correct, on retourne l'instance spécifique de l'utilisateur
            if isinstance(user, Marchand):
                return Marchand.objects(id=user.id).first()  # Récupérer l'objet Marchand spécifique
            elif isinstance(user, Client):
                return Client.objects(id=user.id).first()  # Récupérer l'objet Client spécifique
            else:
                return user  # Si c'est un utilisateur générique, on le retourne tel quel
        return None  # Mauvais mot de passe

