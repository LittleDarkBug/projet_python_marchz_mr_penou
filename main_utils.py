from core.services.AuthService import AuthManager
from demos.achat_client import demo_achats
from demos.historiques import demo_historique
from demos.optimisation_recherche import demo_optimisation_recherche
from demos.espace_marche import demo_espace_marche
import time
from demos.marchands_produits import demo_creation_marche_et_marchands

class Session:
    def __init__(self):
        self.utilisateur_connecte = False
        self.utilisateur_auth = None
        self.role_utilisateur = None

    def se_connecter(self):
        """Permet à l'utilisateur de se connecter."""
        if self.utilisateur_connecte:
            print("Vous êtes déjà connecté.")
            return
        
        username = input("Entrez votre nom d'utilisateur: ")
        password = input("Entrez votre mot de passe: ")
        
        auth_manager = AuthManager()
        self.utilisateur_auth = auth_manager.authenticate_user(username, password)
        
        if self.utilisateur_auth:
            self.utilisateur_connecte = True
            self.role_utilisateur = self.utilisateur_auth.__class__.__name__.lower()  # Identifie le rôle par le nom de la classe
            print(f"Connexion réussie en tant que {self.role_utilisateur.capitalize()}.")
            self.gerer_menu_principal()
        else:
            print("Nom d'utilisateur ou mot de passe incorrect.")

    def afficher_menu_principal(self):
        """Affiche le menu principal après connexion selon le rôle."""
        if self.role_utilisateur == "admin":
            print("""
            -----------------------------------
            Menu Admin
            -----------------------------------
            1. Gérer les démonstrations
            2. Autres actions admin
            3. Se déconnecter
            -----------------------------------
            """)
        elif self.role_utilisateur == "marchand":
            print("""
            -----------------------------------
            Menu Marchand
            -----------------------------------
            1. Gérer les démonstrations
            2. Autres actions marchand
            3. Se déconnecter
            -----------------------------------
            """)
        elif self.role_utilisateur == "client":
            print("""
            -----------------------------------
            Menu Client
            -----------------------------------
            1. Gérer les démonstrations
            2. Autres actions client
            3. Se déconnecter
            -----------------------------------
            """)

    def gerer_menu_principal(self):
        """Gère le menu principal après authentification."""
        while True:
            self.afficher_menu_principal()
            choix = input("Veuillez choisir une option (1-3): ")
            if choix == "1":
                self.gerer_menu_demos()  # Accès au menu des démonstrations
            elif choix == "2":
                if self.role_utilisateur == "admin":
                    print("Actions administratives à définir.")
                elif self.role_utilisateur == "marchand":
                    print(f"Actions pour {self.utilisateur_auth.nom}, le marchand.")
                elif self.role_utilisateur == "client":
                    print(f"Actions pour {self.utilisateur_auth.nom}, le client.")
            elif choix == "3":
                print("Déconnexion...")
                self.utilisateur_connecte = False
                self.role_utilisateur = None
                self.utilisateur_auth = None
                break
            else:
                print("Choix invalide. Veuillez choisir une option entre 1 et 3.")

    def afficher_menu_demos(self):
        """Affiche le menu des démonstrations disponibles."""
        print(r"""
        -----------------------------------
        Menu des Démonstrations
        -----------------------------------
        1. Démonstration : Placement des marchands
        2. Démonstration : Creation de marche, marchands, ajouts et retraits de produits.
        3. Démonstration : Optimisation de l'achat pour un client
        4. Démonstration : Achat client
        5. Démonstration : Historique des achats par marchand
        6. Retour au menu principal
        -----------------------------------
        """)
        choix = input("Veuillez choisir une option (1-5): ")
        return choix

    def gerer_menu_demos(self):
        """Gère le menu des démonstrations et exécute la démonstration choisie."""
        while True:
            choix = self.afficher_menu_demos()
            if choix == "1":
                demo_espace_marche()  # Appel de la démonstration
                time.sleep(5)
            elif choix == "2":
                demo_creation_marche_et_marchands()
                time.sleep(5)
            elif choix == "3":
                demo_optimisation_recherche()
                time.sleep(5)
            elif choix == "4":
                demo_achats()
                time.sleep(5)
                break
            elif choix == "5":
                demo_historique()
                time.sleep(5)
                break
            elif choix == "6":
                print("Retour au menu principal.")
                break
            else:
                print("Choix invalide. Veuillez choisir une option entre 1 et 5.")


def afficher_menu():
    """Affiche le menu principal avec un art ASCII pour MrPlenou."""
    print(r"""
        
    ___ ___  ____       ____  _        ___  ____    ___   __ __ 
    |   |   ||    \     |    \| |      /  _]|    \  /   \ |  |  |
    | _   _ ||  D  )    |  o  ) |     /  [_ |  _  ||     ||  |  |
    |  \_/  ||    /     |   _/| |___ |    _]|  |  ||  O  ||  |  |
    |   |   ||    \     |  |  |     ||   [_ |  |  ||     ||  :  |
    |   |   ||  .  \    |  |  |     ||     ||  |  ||     ||     |
    |___|___||__|\_|    |__|  |_____||_____||__|__| \___/  \__,_|
                                                                
        
        -----------------------------------
        1. Demos
        2. Se connecter
        3. Fermer
        -----------------------------------
    """)
    choix = input("Veuillez choisir une option (1-3): ")
    return choix


