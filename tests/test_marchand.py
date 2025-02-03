import unittest
from core.classes.Marchand import Marchand
from core.enums.TypeMarchandEnum import TypeMarchandEnum
from core.classes.Produit import Produit
from core.data.connection import initialize_connection, close_connection

class TestMarchand(unittest.TestCase):
    
    def setUp(self):
        """Initialisation d'un marché et d'un marchand pour les tests."""
        # Connexion à la base de données MongoDB
        initialize_connection(database_name='mrplenou_tests')

        # Suppression des données existantes
        Marchand.objects.delete()
        Produit.objects.delete()
        
        # Initialisation du marchand
        self.marchand = Marchand(
            nom="Dohi", prenom="Azalakapinhou", telephone="0123456789", adresse="1 rue de Vogan",
            description="Vendeur de fruits", type_marchand=TypeMarchandEnum.GROSSISTE.value,
            username="XXXX", password="XXXXXXXXXXXXX"
        )

        # Initialisation d'un produit à ajouter et retirer
        self.produit = Produit(libelle="Pomme", prix_vente=100, prix_achat=50, quantite=50)
        self.produit.save()

    def test_initialisation_marchand(self):
        """Vérifie que le marchand est initialisé correctement."""
        self.assertEqual(self.marchand.nom, "Dohi")
        self.assertEqual(self.marchand.prenom, "Azalakapinhou")
        self.assertEqual(self.marchand.telephone, "0123456789")
        self.assertEqual(self.marchand.adresse, "1 rue de Vogan")
        self.assertEqual(self.marchand.description, "Vendeur de fruits")
        self.assertEqual(self.marchand.type_marchand, TypeMarchandEnum.GROSSISTE.value)
        self.assertEqual(self.marchand.x, 0)
        self.assertEqual(self.marchand.y, 0)

    def test_save(self):
        """Vérifie que la méthode save fonctionne correctement."""
        self.marchand.save()
        self.assertIsNotNone(self.marchand.id)

    def test_ajout_produit(self):
        """Vérifie que l'ajout d'un produit fonctionne correctement."""
        self.marchand.ajouter_produit(self.produit)
        self.assertIn(self.produit, self.marchand.produits)

    def test_ajout_produit_deja_present(self):
        """Vérifie que l'ajout d'un produit déjà présent soulève une exception."""
        self.marchand.ajouter_produit(self.produit)
        with self.assertRaises(ValueError):
            self.marchand.ajouter_produit(self.produit)

    def test_retrait_produit(self):
        """Vérifie que le retrait d'un produit fonctionne correctement."""
        self.marchand.ajouter_produit(self.produit)
        self.marchand.retirer_produit(self.produit)
        self.assertNotIn(self.produit, self.marchand.produits)

    def test_retrait_produit_inexistant(self):
        """Vérifie que le retrait d'un produit inexistant soulève une exception."""
        with self.assertRaises(ValueError):
            self.marchand.retirer_produit(self.produit)


    def tearDown(self):
        """Ferme la connexion MongoDB après chaque test."""
        close_connection()

if __name__ == '__main__':
    unittest.main()
