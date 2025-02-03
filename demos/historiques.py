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

def demo_historique():
    """
    Démonstration complète de la création d'un marché, l'ajout de marchands et de produits,
    l'achat par un client et la génération d'une facture, suivi des ventes et des statistiques par marchand.
    """
    initialize_connection()
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

    # Simulation de ventes
    for _ in range(10):  # Simuler 10 ventes
        marchand = random.choice(marchands)
        quantites_achetees = {random.choice(produits): random.randint(1, 3) for _ in range(2)}  # Acheteur choisit 2 produits
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
        
        facture = FactureVente(
            prix_total=total_prix, numero_vente=f"V{random.randint(10000, 99999)}", date_vente=datetime.now(),
            modalite=ModaliteVenteEnum.EN_LIGNE.value, lignes=lignes_vente, acheteur=client
        )
        facture.save()
        client.add_achat(facture)
        client.save()

    # Affichage de l'historique des ventes et des statistiques
    print("\nHistorique des ventes par marchand :")
    print("=" * 60)
    print(f"{'Nom du Marchand':<30} {'Produit':<20} {'Quantité':<10} {'Total Ventes':<15}")
    print("=" * 60)

    for marchand in marchands:
        marchand.reload()
        total_ventes_marchand = 0
        for produit in marchand.produits:
            ventes_par_produit = 0
            for facture in FactureVente.objects:
                for ligne in facture.lignes:
                    if ligne.produit == produit:
                        ventes_par_produit += ligne.quantite
            total_ventes_marchand += ventes_par_produit * produit.prix_vente
            # Affichage des ventes par produit
            print(f"{marchand.nom:<30} {produit.libelle:<20} {ventes_par_produit:<10} {ventes_par_produit * produit.prix_vente:<15}")
        
        # Affichage du total des ventes du marchand
        print("-" * 60)
        print(f"{'Total Ventes (marchand)':<50} {total_ventes_marchand:<15}")
        print("=" * 60)
    
    # Affichage du marché
    print(espace_marche)

if __name__ == "__main__":
    demo_historique()
