import random
from core.classes.EspaceMarche import EspaceMarche
from core.classes.Marchand import Marchand
from core.classes.Produit import Produit
from core.enums.TypeMarchandEnum import TypeMarchandEnum
from core.data.connection import initialize_connection, close_connection
from core.utils.Recommandation import optimiser_achats  # Supposons que cette fonction est déjà importée

def demo_optimisation_recherche():
    """
    Démonstration de la création d'un espace de marché, de l'ajout de marchands, 
    de produits, de la recherche de produits, de la suppression de produits, 
    et de l'affichage du marché avec optimisation des achats.
    """

    # Connexion à MongoDB
    initialize_connection()

    # Réinitialisation de la base de données
    EspaceMarche.objects.delete()
    Marchand.objects.delete()
    Produit.objects.delete()

    # Création de l'espace de marché 100x100
    espace_marche = EspaceMarche(nom="Marché Central", taille=(100, 100))
    print(f"Espace de marché '{espace_marche.nom}' créé avec une taille de {espace_marche.taille}")

    # Création de 12 marchands avec des positions aléatoires
    for i in range(10):
        marchand = Marchand(
            nom=f"Marchand_{i+1}", prenom=f"Vendeur_{i+1}", telephone=f"0000{i+1}0000", 
            adresse=f"{i+1} Rue de Exemple", description="Marchand générique", 
            type_marchand=TypeMarchandEnum.DETAILLANT.value, username=f"user{i+1}", password="securepassword"
        )
        # Position aléatoire dans l'espace marché
        x, y = random.randint(0, 99), random.randint(0, 99)
        espace_marche.ajouter_marchand(marchand, x, y)
        marchand.save_marchand()
        

        print(f"Marchand {marchand.nom} ajouté à la position ({x}, {y}).")

    # Création de 500 produits répartis entre les marchands

    produits = []
    
    for i in range(3,100):
        produit = Produit(libelle=f"Produit_{i%4}", prix_vente=random.randint(1, 200), 
                          prix_achat=random.randint(1, 100), quantite=random.randint(1, 50))
        produits.append(produit)
        produit.save()
        marchand = Marchand.objects.get(id=random.choice(Marchand.objects.all()).id)
        marchand.ajouter_produit(produit)
        
        
    print("100 produits créés et ajoutés aux marchands.")

    # Recherche de produits spécifiques par un client et optimisation des achats
    produits_recherches = {
        "Produit_1": 1,
        "Produit_2": 2,
        "Produit_3": 1
    }
    
    print("\nOptimisation des achats pour le client (position: 50, 50) avec les produits recherchés.")
    marchands_recommandes = optimiser_achats(50, 50, produits_recherches)

    if len(marchands_recommandes) > 0:
        print("Marchands recommandés pour les produits recherchés:")
        for marchand in marchands_recommandes:
            print(f"Nom: {marchand["marchand"].nom}, Distance: {marchand["distance"]}, Niveau de stock: {marchand["total_prix"]}")
        
    else:
        print("Aucun marchand trouvé pour les produits recherchés.")

    # Suppression d'un produit
    print("\nSuppression du produit 'Produit_1' du premier marchand.")
    premier_marchand = Marchand.objects.first()
    produit_a_supprimer = premier_marchand.produits[0]  # Supposons qu'il a au moins un produit
    premier_marchand.retirer_produit(produit_a_supprimer)

    # Affichage de l'espace de marché après modifications
    print("\nAffichage de l'espace de marché après modifications :")
    print(espace_marche)

    # Déconnexion de la base de données
    close_connection()

if __name__ == "__main__":
    demo_optimisation_recherche()
