from core.data.connection import initialize_connection
from core.services.AuthService import AuthManager
from core.classes.Utilisateur import Utilisateur
from core.classes.Admin import Admin  # Si vous avez une classe Admin qui hérite d'Utilisateur
from core.utils.PasswordUtils import PasswordUtils

def initialiser_admin():
    initialize_connection()
    """Vérifie si un administrateur existe et le crée si nécessaire."""
    admin_existant = Admin.find_one({'username': 'admin'})  # Vérifie si un admin existe déjà
    if admin_existant:
        print("L'administrateur existe déjà.")
    else:
        # Si l'administrateur n'existe pas, on le crée
        admin = Admin(
            nom='Admin',
            prenom='System',
            telephone='0123456789',
            adresse='1 rue de l\'administration',
            username='admin',
            password='admin' 
        ) # Hash du mot de passe
        admin.save()  # Sauvegarde l'administrateur dans la base de données
        print("Administrateur par défaut créé.")

# Exécution de l'initialisation à chaque démarrage
if __name__ == "__main__":
    initialiser_admin()
