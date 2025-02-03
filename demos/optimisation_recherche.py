import random
from core.classes.EspaceMarche import EspaceMarche
from core.classes.Marchand import Marchand
from core.classes.Produit import Produit
from core.enums.TypeMarchandEnum import TypeMarchandEnum
from core.data.connection import initialize_connection, close_connection
from core.utils.Recommandation import optimiser_achats  # Supposons que cette fonction est déjà importée
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

def demo_optimisation_recherche():
    """
    Démonstration de la création d'un espace de marché, de l'ajout de marchands, 
    de produits, de la recherche de produits, de la suppression de produits, 
    et de l'affichage du marché avec optimisation des achats.
    """
    console = Console()

    # Connexion à MongoDB
    with console.status("[bold green]Connexion à la base de données..."):
        initialize_connection(database_name='mrplenou_demo')

    # Réinitialisation de la base de données
    with console.status("[bold yellow]Réinitialisation de la base de données..."):
        EspaceMarche.objects.delete()
        Marchand.objects.delete()
        Produit.objects.delete()

    # Création de l'espace de marché 100x100
    espace_marche = EspaceMarche(nom="Marché Central", taille=(100, 100))
    rprint(Panel(f"[bold green]Espace de marché '{espace_marche.nom}' créé avec une taille de {espace_marche.taille}"))

    # Création des marchands
    table_marchands = Table(title="Marchands créés")
    table_marchands.add_column("Nom", style="cyan")
    table_marchands.add_column("Position", style="magenta")

    with console.status("[bold blue]Création des marchands..."):
        for i in range(10):
            marchand = Marchand(
                nom=f"Marchand_{i+1}", prenom=f"Vendeur_{i+1}", telephone=f"0000{i+1}0000", 
                adresse=f"{i+1} Rue de Exemple", description="Marchand générique", 
                type_marchand=TypeMarchandEnum.DETAILLANT.value, username=f"user{i+1}", password="securepassword"
            )
            x, y = random.randint(0, 99), random.randint(0, 99)
            espace_marche.ajouter_marchand(marchand, x, y)
            marchand.save_marchand()
            table_marchands.add_row(marchand.nom, f"({x}, {y})")

    console.print(table_marchands)

    # Création des produits
    with console.status("[bold blue]Création des produits..."):
        for i in range(3,100):
            produit = Produit(libelle=f"Produit_{i%4}", prix_vente=random.randint(1, 200), 
                            prix_achat=random.randint(1, 100), quantite=random.randint(1, 50))

            produit.save()
            marchand = Marchand.objects.get(id=random.choice(Marchand.objects.all()).id)
            marchand.ajouter_produit(produit)

    rprint("[bold green]100 produits créés et ajoutés aux marchands.")

    # Recherche et optimisation
    produits_recherches = {
        "Produit_1": 1,
        "Produit_2": 2,
        "Produit_3": 1
    }
    
    console.print("\n[bold]Optimisation des achats[/bold]", style="yellow")
    console.print("Position client: (50, 50)")
    console.print("Produits recherchés:", style="cyan")
    for prod, qte in produits_recherches.items():
        console.print(f"- {prod}: {qte}", style="cyan")

    marchands_recommandes = optimiser_achats(50, 50, produits_recherches)

    if len(marchands_recommandes) > 0:
        table_recommandations = Table(title="Marchands recommandés")
        table_recommandations.add_column("Nom", style="cyan")
        table_recommandations.add_column("Distance", style="magenta")
        table_recommandations.add_column("Prix total", style="green")

        for marchand in marchands_recommandes:
            table_recommandations.add_row(
                marchand["marchand"].nom,
                f"{marchand['distance']:.2f}",
                f"{marchand['total_prix']:.2f} FCFA"
            )
        console.print(table_recommandations)
    else:
        console.print("[red]Aucun marchand trouvé pour les produits recherchés.")

    # Déconnexion
    with console.status("[bold red]Déconnexion de la base de données..."):
        close_connection()

if __name__ == "__main__":
    demo_optimisation_recherche()
