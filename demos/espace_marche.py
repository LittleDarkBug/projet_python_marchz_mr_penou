from core.classes.EspaceMarche import EspaceMarche
from core.classes.Marchand import Marchand
from core.enums.TypeMarchandEnum import TypeMarchandEnum
from core.data.connection import initialize_connection, close_connection
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def demo_espace_marche():
    """
    Démonstration du placement des marchands dans un espace de marché.
    """
    console.print("\n[bold magenta]=== Démonstration : Placement des marchands ===[/bold magenta]")
    
    # Initialisation de la connexion MongoDB
    initialize_connection(database_name='mrplenou_demo')

    # Suppression de la base de données
    Marchand.objects.delete()
    EspaceMarche.objects.delete()

    # Créer un espace de marché de taille 15x15
    espace_marche = EspaceMarche(nom="Marché ASSIGAME", taille=(15, 15))
    console.print(f"[bold green]Espace de marché créé :[/bold green] {espace_marche.nom} [dim]de taille {espace_marche.taille}[/dim]")

    # Créer quelques marchands
    marchand1 = Marchand(
        nom="Dupont",
        prenom="Jean",
        telephone="123456789",
        adresse="1 Rue de la Paix",
        username="jdupont",
        password="password123",
        description="Vendeur de fruits et légumes",
        type_marchand=TypeMarchandEnum.GROSSISTE.value  # Type : Grossiste
    ).save_marchand()

    marchand2 = Marchand(
        nom="Martin",
        prenom="Marie",
        telephone="987654321",
        adresse="2 Avenue des Fleurs",
        username="mmartin",
        password="password456",
        description="Vendeuse de vêtements",
        type_marchand=TypeMarchandEnum.DETAILLANT.value  # Type : Détaillant
    ).save_marchand()

    marchand3 = Marchand(
        nom="Leroy",
        prenom="Luc",
        telephone="555555555",
        adresse="3 Boulevard des Artisans",
        username="lleroy",
        password="password789",
        description="Vendeur de bijoux",
        type_marchand=TypeMarchandEnum.MIXTE.value  # Type : Mixte
    ).save_marchand()

    # Ajouter les marchands à l'espace de marché
    try:
        espace_marche.ajouter_marchand(marchand1, x=2, y=3)
        espace_marche.ajouter_marchand(marchand2, x=5, y=7)
        espace_marche.ajouter_marchand(marchand3, x=8, y=1)
        console.print("[bold green]Marchands ajoutés avec succès ![/bold green]")
    except ValueError as e:
        console.print(f"[bold red]Erreur[/bold red] lors de l'ajout d'un marchand : {e}")

    # Afficher les emplacements libres
    emplacements_libres = espace_marche.obtenir_emplacements_libres()
    console.print(f"\n[bold yellow]Emplacements libres restants : {len(emplacements_libres)}[/bold yellow]")

    # Afficher l'espace de marché avec les marchands
    console.print("\n[bold cyan]Affichage de l'espace de marché dans votre navigateur:[/bold cyan]")
    console.print(Panel(str(espace_marche), title="Espace de Marché", border_style="blue"))

    # Sauvegarder l'espace de marché dans MongoDB
    espace_marche.save()
    console.print("[bold green]Espace de marché sauvegardé dans la base de données.[/bold green]")

    # Fermer la connexion MongoDB
    close_connection()

if __name__ == "__main__":
    demo_espace_marche()
