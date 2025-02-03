from analyse_de_donnees.analyse_donees import analyser_donnees, demo_analyse_donnees
from init_admin import initialiser_admin
from main_utils import Session, afficher_menu
import time
from rich.console import Console

console = Console()

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
            demo_analyse_donnees()
            console.print("[bold green]Analyse des données terminée , Les diagrammes sont ouverts dans votre navigateur.[/bold green]")
            time.sleep(10)
        elif choix == "4":
            session.fermer()
            break
        else:
            print("Choix invalide. Veuillez choisir une option entre 1 et 3.")

if __name__ == "__main__":
    main()
