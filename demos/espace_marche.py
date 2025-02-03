from core.classes.EspaceMarche import EspaceMarche
from core.classes.Marchand import Marchand
from core.enums.TypeMarchandEnum import TypeMarchandEnum
from core.data.connection import initialize_connection, close_connection
from rich import print

def demo_espace_marche():
    """
    Démonstration du placement des marchands dans un espace de marché.
    """
    print("\n=== Démonstration : Placement des marchands ===")
    
    # Initialisation de la connexion MongoDB
    initialize_connection(host='localhost', port=27017, database_name='mrplenou', username='admin', password='admin')

    #Supression de la base de données
    Marchand.objects.delete()
    EspaceMarche.objects.delete()

    # Créer un espace de marché de taille 15x15
    espace_marche = EspaceMarche(nom="Marché ASSIGAME", taille=(15, 15))
    print(f"Espace de marché créé : {espace_marche.nom} de taille {espace_marche.taille}")

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
        print("Marchands ajoutés avec succès !")
    except ValueError as e:
        print(f"Erreur lors de l'ajout d'un marchand : {e}")

    # Afficher les emplacements libres
    emplacements_libres = espace_marche.obtenir_emplacements_libres()
    print(f"\nEmplacements libres restants : {len(emplacements_libres)}")

    # Afficher l'espace de marché avec les marchands
    print("\nAffichage de l'espace de marché :")
    print(espace_marche)

    # Sauvegarder l'espace de marché dans MongoDB
    espace_marche.save()
    print("Espace de marché sauvegardé dans la base de données.")

    # Fermer la connexion MongoDB
    close_connection()

if __name__ == "__main__":
    demo_espace_marche()

