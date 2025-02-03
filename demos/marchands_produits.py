from core.classes.EspaceMarche import EspaceMarche
from core.classes.Marchand import Marchand
from core.classes.Produit import Produit
from core.enums.TypeMarchandEnum import TypeMarchandEnum
from core.data.connection import initialize_connection, close_connection
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

def demo_creation_marche_et_marchands():
    """
    Démonstration de la création d'un espace de marché, de l'ajout de marchands, 
    de produits, de la recherche de produits, de la suppression de produits 
    et de l'affichage du marché.
    """
    # Création de la console Rich
    console = Console()

    # Connexion à MongoDB
    console.print("[bold blue]Connexion à MongoDB...[/bold blue]")
    initialize_connection(database_name='mrplenou_demo')
    #reinitialisation de la base de données
    console.print("[bold yellow]Réinitialisation de la base de données...[/bold yellow]")
    EspaceMarche.objects.delete()
    Marchand.objects.delete()
    Produit.objects.delete()

    # Création de l'espace de marché
    espace_marche = EspaceMarche(nom="Marché Central", taille=(5, 5))
    console.print(Panel(f"Espace de marché '[bold green]{espace_marche.nom}[/bold green]' créé avec une taille de {espace_marche.taille}", title="Création du marché"))

    # Création des marchands
    marchand_1 = Marchand(
        nom="Dupont", prenom="Pierre", telephone="123456789", adresse="1 Rue de Paris", 
        description="Marchand de fruits", type_marchand=TypeMarchandEnum.DETAILLANT.value, 
        username="pdupont", password="securepassword1"
    )
    marchand_2 = Marchand(
        nom="Lemoine", prenom="Julie", telephone="987654321", adresse="2 Rue de Lyon", 
        description="Marchand de légumes", type_marchand=TypeMarchandEnum.DETAILLANT.value, 
        username="jlemoine", password="securepassword2"
    )

    marchand_1.save_marchand()
    marchand_2.save_marchand()

    # Ajout des marchands à l'espace de marché
    espace_marche.ajouter_marchand(marchand_1, 2, 3)
    espace_marche.ajouter_marchand(marchand_2, 4, 4)

    print(f"Marchand {marchand_1.nom} ajouté à la position (2, 3).")
    print(f"Marchand {marchand_2.nom} ajouté à la position (4, 4).")

    # Création et ajout des produits
    produits_table = Table(title="Produits ajoutés")
    produits_table.add_column("Libellé", style="cyan")
    produits_table.add_column("Prix de vente", style="green")
    produits_table.add_column("Quantité", style="yellow")
    produits_table.add_column("Marchand", style="magenta")

    produit_1 = Produit(libelle="Pomme", prix_vente=100, prix_achat=50, quantite=100)
    produit_2 = Produit(libelle="Carotte", prix_vente=30, prix_achat=15, quantite=200)

    produit_1.save()
    produit_2.save()

    # Ajout des produits aux marchands
    marchand_1.ajouter_produit(produit_1)
    marchand_2.ajouter_produit(produit_2)

    print(f"Produit '{produit_1.libelle}' ajouté au marchand {marchand_1.nom}.")
    print(f"Produit '{produit_2.libelle}' ajouté au marchand {marchand_2.nom}.")

    produits_table.add_row(
        produit_1.libelle,
        f"{produit_1.prix_vente}FCFA",
        str(produit_1.quantite),
        marchand_1.nom
    )
    produits_table.add_row(
        produit_2.libelle,
        f"{produit_2.prix_vente}FCFA",
        str(produit_2.quantite),
        marchand_2.nom
    )
    console.print(produits_table)

    # Recherche d'un produit
    console.print("\n[bold]Recherche du produit 'Pomme' :[/bold]")
    produit_trouves = marchand_1.rechercher_produit("Pomme")
    if produit_trouves:
        for produit_trouve in produit_trouves:
            console.print(f"✅ Produit trouvé : [cyan]{produit_trouve.libelle}[/cyan], Prix de vente : [green]{produit_trouve.prix_vente}FCFA[/green]")
    else:
        console.print("❌ Produit non trouvé.", style="red")

    # Suppression d'un produit
    console.print("\n[bold red]Suppression du produit 'Carotte' du marchand Lemoine.[/bold red]")
    marchand_2.retirer_produit(produit_2)

    # Affichage de l'espace de marché
    console.print("\n[bold]Affichage de l'espace de marché dans le navigateur après modifications  :[/bold]")
    console.print(Panel(str(espace_marche), title="État final du marché"))

    # Déconnexion de la base de données
    console.print("[bold blue]Déconnexion de la base de données...[/bold blue]")
    close_connection()

if __name__ == "__main__":
    demo_creation_marche_et_marchands()
