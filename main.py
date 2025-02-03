from init_admin import initialiser_admin
from main_utils import Session, afficher_menu
def main():
    initialiser_admin()
    session = Session()
    
    while True:
        choix = afficher_menu()
        if choix == "1":
            session.gerer_menu_demos()
        elif choix == "2":
            session.se_connecter()
        elif choix == "3":
            session.fermer()
            break
        else:
            print("Choix invalide. Veuillez choisir une option entre 1 et 3.")

if __name__ == "__main__":
    main()
