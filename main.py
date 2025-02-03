from main_utils import afficher_menu, gerer_menu_demos

def main():
    while True:
        choix = afficher_menu()
        if choix == "1":
            gerer_menu_demos()
        elif choix == "2":
            pass
        elif choix == "3":
            pass
        else:
            print("Choix invalide. Veuillez choisir une option entre 1 et 3.")

if __name__ == "__main__":
    main()
