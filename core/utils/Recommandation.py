import math
from core.classes.Marchand import Marchand
from core.classes.Produit import Produit
from core.classes.Client import Client
from core.data.connection import initialize_connection
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

# Fonction pour calculer la distance euclidienne
def distance_euclidienne(x1, y1, x2, y2):
    """Calcul de la distance euclidienne entre deux points (x1, y1) et (x2, y2)."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Fonction pour optimiser les achats
def optimiser_achats(x, y, produits_recherches):
    """
    Optimiser les achats pour un client en fonction des produits recherchés, prix et distance.
    
    :param x : x actuel du client 
    :param y: y actuel du client
    :param produits_recherches: Dictionnaire {nom_du_produit: quantité} des produits recherchés par le client.
    :return: Liste des marchands recommandés triés par distance puis par prix.
    """
    console = Console()
    marchands_recommandes = []

    # Connexion à la base de données pour récupérer les marchands
    initialize_connection()
    marchands = Marchand.objects.select_related()

    with console.status("[bold green]Recherche des meilleurs marchands..."):
        for marchand in marchands:
            marchand.reload()
            total_prix = 0
            produits_disponibles = []

            # Vérification des produits disponibles pour chaque marchand
            for produit_nom, quantite_recherchee in produits_recherches.items():
                produit = next((p for p in marchand.produits if p.libelle == produit_nom), None)
                if produit and produit.quantite >= quantite_recherchee:
                    total_prix += produit.prix_vente * quantite_recherchee
                    produits_disponibles.append(produit_nom)
                else:
                    break
            else:
                # Si tous les produits sont trouvés, calculer la distance et ajouter le marchand à la liste
                distance = distance_euclidienne(x, y, marchand.x, marchand.y)
                marchands_recommandes.append({
                    "marchand": marchand,
                    "distance": distance,
                    "total_prix": total_prix
                })

    # Trier les marchands par distance (croissante) et prix total (croissant)
    marchands_recommandes.sort(key=lambda x: (x["distance"], x["total_prix"]))

    # Création d'un tableau Rich pour afficher les résultats
    table = Table(title="Recommandations de Marchands", show_header=True, header_style="bold magenta")
    table.add_column("Marchand", style="cyan")
    table.add_column("Distance", justify="right", style="green")
    table.add_column("Prix Total", justify="right", style="yellow")
    table.add_column("Produits Disponibles", style="blue")

    for recommandation in marchands_recommandes:
        table.add_row(
            recommandation["marchand"].nom,
            f"{recommandation['distance']:.2f} km",
            f"{recommandation['total_prix']:.2f} FCFA",
            ", ".join(produits_recherches.keys())
        )

    console.print("\n")
    console.print(Panel.fit(
        Text("🎯 Résultats de la recherche", style="bold white"),
        border_style="green"
    ))
    console.print(table)

    return marchands_recommandes

