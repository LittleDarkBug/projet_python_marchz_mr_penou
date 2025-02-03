from core.classes.EspaceMarche import EspaceMarche
from core.classes.Marchand import Marchand
from core.classes.Produit import Produit
from core.enums.TypeMarchandEnum import TypeMarchandEnum
from core.data.connection import initialize_connection, close_connection

def demo_creation_marche_et_marchands():
    """
    Démonstration de la création d'un espace de marché, de l'ajout de marchands, 
    de produits, de la recherche de produits, de la suppression de produits 
    et de l'affichage du marché.
    """

    # Connexion à MongoDB
    initialize_connection()

    #reinitialisation de la base de données
    EspaceMarche.objects.delete()
    Marchand.objects.delete()
    Produit.objects.delete()

    # Création de l'espace de marché
    espace_marche = EspaceMarche(nom="Marché Central", taille=(5, 5))
    print(f"Espace de marché '{espace_marche.nom}' créé avec une taille de {espace_marche.taille}")

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

    # Création de produits
    produit_1 = Produit(libelle="Pomme", prix_vente=100, prix_achat=50, quantite=100)
    produit_2 = Produit(libelle="Carotte", prix_vente=30, prix_achat=15, quantite=200)

    produit_1.save()
    produit_2.save()

    # Ajout des produits aux marchands
    marchand_1.ajouter_produit(produit_1)
    marchand_2.ajouter_produit(produit_2)

    print(f"Produit '{produit_1.libelle}' ajouté au marchand {marchand_1.nom}.")
    print(f"Produit '{produit_2.libelle}' ajouté au marchand {marchand_2.nom}.")

    # Recherche d'un produit
    print("\nRecherche du produit 'Pomme' :")
    produit_trouves = marchand_1.rechercher_produit("Pomme")
    if produit_trouves:
        for produit_trouve in produit_trouves:
            print(f"Produit trouvé : {produit_trouve.libelle}, Prix de vente : {produit_trouve.prix_vente}€")
    else:
        print("Produit non trouvé.")

    # Suppression d'un produit
    print("\nSuppression du produit 'Carotte' du marchand Lemoine.")
    marchand_2.retirer_produit(produit_2)

    # Affichage de l'espace de marché
    print("\nAffichage de l'espace de marché après modifications :")
    print(espace_marche)

    # Déconnexion de la base de données
    close_connection()

if __name__ == "__main__":
    demo_creation_marche_et_marchands()
