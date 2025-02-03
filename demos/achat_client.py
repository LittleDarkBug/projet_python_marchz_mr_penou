import random
from datetime import datetime
from mongoengine import connect
from core.classes.EspaceMarche import EspaceMarche
from core.classes.Marchand import Marchand
from core.classes.Produit import Produit
from core.classes.Client import Client
from core.classes.LigneVente import LigneVente
from core.classes.FactureVente import FactureVente
from core.enums.ModaliteVenteEnum import ModaliteVenteEnum
from core.data.connection import initialize_connection
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def demo_achats():
    """
    Démonstration complète de la création d'un marché, l'ajout de marchands et de produits,
    l'achat par un client et la génération d'une facture.
    """
    initialize_connection(database_name='mrplenou_demo')
    # Réinitialisation de la base de données
    EspaceMarche.objects.delete()
    Marchand.objects.delete()
    Produit.objects.delete()
    Client.objects.delete()
    FactureVente.objects.delete()
    LigneVente.objects.delete()

    # Création de l'espace de marché
    espace_marche = EspaceMarche(nom="Marché Central", taille=[50, 50])
    espace_marche.save()

    # Ajout de marchands avec des positions aléatoires
    marchands = []
    for i in range(3):
        marchand = Marchand(
            nom=f"Marchand_{i+1}", prenom=f"Vendeur_{i+1}", telephone=f"060000000{i}",
            adresse=f"{i+1} Rue du Commerce", username=f"marchand{i+1}", password="pass1234",
            type_marchand="Fruits"
        )
        x, y = random.randint(0, 49), random.randint(0, 49)
        espace_marche.ajouter_marchand(marchand, x, y)
        marchand.save()
        marchands.append(marchand)
    espace_marche.save()

    # Ajout de produits aux marchands
    produits = []
    for i in range(10):
        produit = Produit(
            libelle=f"Produit_{i+1}", prix_achat=random.randint(10, 50), prix_vente=random.randint(60, 100),
            description=f"Produit_{i+1} description", quantite=random.randint(5, 20)
        )
        produit.save()
        marchand = random.choice(marchands)
        marchand.ajouter_produit(produit)
        marchand.save()
        produits.append(produit)

    # Création d'un client
    client = Client(username="client1", password="clientpass", nom="Doe", prenom="John", telephone="0612345678", adresse="123 Rue de la Ville")
    client.save()

    # Simulation d'un achat
    quantites_achetees = {produits[0]: 2, produits[1]: 3}
    lignes_vente = []
    total_prix = 0

    for produit, quantite in quantites_achetees.items():
        if produit.quantite >= quantite:
            produit.quantite -= quantite
            produit.save()
            prix_total_ligne = quantite * produit.prix_vente
            ligne = LigneVente(quantite=quantite, prix_total_ligne=prix_total_ligne, produit=produit)
            ligne.save()
            lignes_vente.append(ligne)
            total_prix += prix_total_ligne

    # Création de la facture
    facture = FactureVente(
        prix_total=total_prix, numero_vente="V12345", date_vente=datetime.now(),
        modalite=ModaliteVenteEnum.EN_LIGNE.value, lignes=lignes_vente, acheteur=client
    )
    facture.save()
    client.add_achat(facture)
    client.save()

    # Affichage stylisé de la facture
    console.print("\n[bold green]Facture générée :[/bold green]", style="bold white")
    console.print(facture, style="italic cyan")

    # Affichage du stock restant des marchands dans un tableau
    console.print("\n[bold yellow]Stock restant des marchands :[/bold yellow]")
    table = Table(title="Stocks des Marchands", caption="Quantité des produits restants")
    table.add_column("Nom du Marchand", style="cyan", width=20)
    table.add_column("Produit", style="magenta", width=30)
    table.add_column("Quantité", justify="right", style="green")

    for marchand in marchands:
        marchand.reload()
        for produit in marchand.produits:
            table.add_row(marchand.nom, produit.libelle, str(produit.quantite))

    console.print(table)

    # Affichage du marché
    console.print("\n[bold cyan]Espace Marché :[/bold cyan]", style="bold white")
    console.print(espace_marche, style="italic yellow")

if __name__ == "__main__":
    demo_achats()
