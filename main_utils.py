from demos.achat_client import demo_achats
from demos.historiques import demo_historique
from demos.optimisation_recherche import demo_optimisation_recherche
from demos.espace_marche import demo_espace_marche
from dependency_injector.wiring import inject, Provide
import time

from demos.marchands_produits import demo_creation_marche_et_marchands

def afficher_menu():
    """Affiche le menu principal avec un art ASCII pour MrPlenou."""
    print("""
    
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


def se_connecter():
    """Permet à l'utilisateur de se connecter."""
    if utilisateur_connecte:
        print("Vous êtes déjà connecté.")
        return
    username = input("Entrez votre nom d'utilisateur: ")
    password = input("Entrez votre mot de passe: ")
    # Pour la démonstration, on peut utiliser des informations fixes
    if username == "admin" and password == "password":
        utilisateur_connecte = True
        print("Connexion réussie.")
    else:
        print("Nom d'utilisateur ou mot de passe incorrect.")

def fermer():
    """Ferme le programme."""
    print("Fermeture du programme.")
    exit()

@inject
def afficher_menu_demos():
    """
    Affiche le menu des démonstrations disponibles.
    """
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

@inject
def gerer_menu_demos():
    """
    Gère le menu des démonstrations et exécute la démonstration choisie.
    """
    while True:
        choix = afficher_menu_demos()
        if choix == "1":
            demo_espace_marche()  # Appel de la démonstration
            #Attendre 15 secondes
            time.sleep(5)
        elif choix == "2":
            demo_creation_marche_et_marchands()
            time.sleep(5)
            # Ajouter une autre démonstration ici
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
