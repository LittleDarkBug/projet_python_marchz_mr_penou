import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
from rich.console import Console
from rich.panel import Panel
from core.data.connection import initialize_connection, close_connection
from core.classes.Marchand import Marchand
from core.classes.Produit import Produit
from core.classes.EspaceMarche import EspaceMarche
from core.classes.FactureVente import FactureVente
from core.classes.LigneVente import LigneVente
from core.classes.Fournisseur import Fournisseur
from core.enums.TypeMarchandEnum import TypeMarchandEnum
import time

console = Console()

def generer_donnees_test():
    """Génère un grand nombre de données de test."""
    # Initialiser la connexion à une nouvelle base de données pour les tests
    initialize_connection(database_name='mrplenou_analyse')
    
    
    # Nettoyer la base de données
    Marchand.objects.delete()
    Produit.objects.delete()
    EspaceMarche.objects.delete()
    FactureVente.objects.delete()
    LigneVente.objects.delete()
    Fournisseur.objects.delete()

    # Créer des fournisseurs
    fournisseurs = []
    for i in range(5):
        fournisseur = Fournisseur(
            nom=f"Fournisseur {i+1}",
            adresse=f"Adresse {i+1}",
            telephone=f"123456789{i}",
            email=f"fournisseur{i+1}@example.com"
        ).save()
        fournisseurs.append(fournisseur)

    # Créer un marché
    marche = EspaceMarche(nom="Grand Marché", taille=[20, 20]).save()

    # Créer des marchands
    marchands = []
    types_marchand = [t.value for t in TypeMarchandEnum]
    for i in range(10):
        marchand = Marchand(
            nom=f"Marchand {i+1}",
            prenom=f"Prénom {i+1}",
            telephone=f"987654321{i}",
            adresse=f"Adresse Marchand {i+1}",
            username=f"marchand{i+1}",
            password="password123",
            type_marchand=random.choice(types_marchand),
            x=random.randint(0, 19),
            y=random.randint(0, 19)
        ).save()
        marchands.append(marchand)
        marche.marchands.append(marchand)
    marche.save()

    # Créer des produits et les assigner aux marchands
    produits_par_marchand = {}
    noms_produits = ["Tomates", "Pommes", "Bananes", "Oranges", "Carottes", 
                     "Oignons", "Poivrons", "Concombres", "Mangues", "Ananas"]
    
    for marchand in marchands:
        produits = []
        for _ in range(random.randint(3, 6)):
            produit = Produit(
                libelle=random.choice(noms_produits),
                prix_achat=random.uniform(100, 500),
                prix_vente=random.uniform(600, 1200),
                description="Description du produit",
                quantite=random.randint(10, 100),
                fournisseur=random.choice(fournisseurs)
            ).save()
            produits.append(produit)
            marchand.produits.append(produit)
        marchand.save()
        produits_par_marchand[marchand.id] = produits

    # Générer des ventes sur 30 jours
    date_debut = datetime.now() - timedelta(days=30)
    numero_vente_counter = 1  # Compteur pour les numéros de vente
    
    for jour in range(30):
        date_vente = date_debut + timedelta(days=jour)
        nb_ventes = random.randint(5, 15)
        
        for _ in range(nb_ventes):
            marchand = random.choice(marchands)
            produits_disponibles = produits_par_marchand[marchand.id]
            
            # Créer des lignes de vente
            lignes_vente = []
            total_prix = 0
            
            for _ in range(random.randint(1, 3)):
                produit = random.choice(produits_disponibles)
                quantite = random.randint(1, 5)
                prix_total_ligne = quantite * produit.prix_vente
                
                ligne = LigneVente(
                    quantite=quantite,
                    prix_total_ligne=prix_total_ligne,
                    produit=produit
                ).save()
                lignes_vente.append(ligne)
                total_prix += prix_total_ligne
                
                # Mettre à jour le stock
                produit.quantite = max(0, produit.quantite - quantite)
                produit.save()
            
            # Créer la facture avec un numéro unique
            facture = FactureVente(
                prix_total=total_prix,
                numero_vente=f"V{date_vente.strftime('%Y%m%d')}-{numero_vente_counter:04d}",
                date_vente=date_vente,
                modalite="EN_LIGNE",
                lignes=lignes_vente,
                acheteur=marchand
            ).save()
            
            numero_vente_counter += 1  # Incrémenter le compteur

def analyser_donnees():
    """Analyse les données et génère des visualisations."""
    # 1. Histogramme des produits les plus vendus
    ventes = []
    for ligne in LigneVente.objects():
        ventes.append({
            'produit': ligne.produit.libelle,
            'quantite': ligne.quantite,
            'prix_total': ligne.prix_total_ligne,
            'date_vente': ligne.id.generation_time
        })
    
    df_ventes = pd.DataFrame(ventes)
    
    # Graphique 1: Produits les plus vendus
    fig1 = px.histogram(df_ventes, 
                       x='produit', 
                       y='quantite',
                       title='Produits les plus vendus',
                       labels={'produit': 'Produit', 'quantite': 'Quantité vendue'})
    fig1.show()

    # 2. Répartition des ventes par marchand
    ventes_par_marchand = []
    for facture in FactureVente.objects():
        ventes_par_marchand.append({
            'marchand': f"{facture.acheteur.nom} {facture.acheteur.prenom}",
            'montant': facture.prix_total
        })
    
    df_ventes_marchands = pd.DataFrame(ventes_par_marchand)
    fig2 = px.pie(df_ventes_marchands, 
                  values='montant', 
                  names='marchand',
                  title='Répartition des ventes par marchand')
    fig2.show()

    # 3. Heatmap des niveaux de stock
    stocks = []
    for marchand in Marchand.objects():
        for produit in marchand.produits:
            stocks.append({
                'x': marchand.x,
                'y': marchand.y,
                'stock': produit.quantite
            })
    
    df_stocks = pd.DataFrame(stocks)
    fig3 = px.density_heatmap(df_stocks, 
                             x='x', 
                             y='y', 
                             z='stock',
                             title='Niveaux de stock par position dans le marché')
    fig3.show()

    # 4. Analyse temporelle des ventes
    df_ventes['date'] = pd.to_datetime(df_ventes['date_vente'])
    ventes_quotidiennes = df_ventes.groupby(df_ventes['date'].dt.date)['prix_total'].sum().reset_index()
    
    fig4 = px.line(ventes_quotidiennes, 
                   x='date', 
                   y='prix_total',
                   title='Évolution des ventes quotidiennes',
                   labels={'date': 'Date', 'prix_total': 'Montant total des ventes'})
    fig4.show()

def demo_analyse_donnees():
    """Fonction principale de démonstration de l'analyse des données."""
    console.print(Panel("[bold cyan]Démonstration : Analyse des données[/bold cyan]"))
    
    # Générer les données de test
    console.print("[yellow]Génération des données de test...[/yellow]")
    generer_donnees_test()
    
    # Analyser les données
    console.print("[yellow]Analyse des données et génération des visualisations...[/yellow]")
    analyser_donnees()
    
    console.print("[bold green]Analyse terminée ! Les graphiques ont été générés.[/bold green]")
    
    # Fermer la connexion
    close_connection()

if __name__ == "__main__":
    demo_analyse_donnees()
