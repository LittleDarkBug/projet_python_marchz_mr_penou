import unittest
from core.classes.Marchand import Marchand
from core.classes.EspaceMarche import EspaceMarche
from core.enums.TypeMarchandEnum import TypeMarchandEnum

class TestEspaceMarche(unittest.TestCase):
    
    def setUp(self):
        """Initialisation d'un espace marché et de quelques marchands pour les tests."""
        self.espace_marche = EspaceMarche(nom="Marché Central", taille=(5, 5))  # Un espace de marché de 5x5
        self.marchand_1 = Marchand(nom="Dupont", prenom="Pierre", telephone="123456789", adresse="1 Rue de Paris", description="Marchand de fruits", type_marchand=TypeMarchandEnum.DETAILLANT)
        self.marchand_2 = Marchand(nom="Lemoine", prenom="Julie", telephone="987654321", adresse="2 Rue de Lyon", description="Marchand de légumes", type_marchand=TypeMarchandEnum.DETAILLANT)

    def test_ajouter_marchand_position_libre(self):
        """Test pour l'ajout d'un marchand à une position libre."""
        self.espace_marche.ajouter_marchand(self.marchand_1, 2, 3)
        self.assertEqual(self.marchand_1.x, 2)
        self.assertEqual(self.marchand_1.y, 3)
        self.assertIn(self.marchand_1, self.espace_marche.marchands)

    def test_ajouter_marchand_position_occupee(self):
        """Test pour l'ajout d'un marchand à une position déjà occupée."""
        self.espace_marche.ajouter_marchand(self.marchand_1, 2, 3)
        # Essayer d'ajouter un autre marchand à la même position
        self.espace_marche.ajouter_marchand(self.marchand_2, 2, 3)
        self.assertEqual(self.marchand_2.x, None)  # Il ne doit pas être placé
        self.assertEqual(self.marchand_2.y, None)
        self.assertNotIn(self.marchand_2, self.espace_marche.marchands)

    def test_obtenir_emplacements_libres(self):
        """Test pour obtenir la liste des emplacements libres dans le marché."""
        # Ajouter un marchand à une position
        self.espace_marche.ajouter_marchand(self.marchand_1, 2, 3)
        # Obtenir les emplacements libres
        emplacements_libres = self.espace_marche.obtenir_emplacements_libres()
        self.assertNotIn((2, 3), emplacements_libres)  # La position (2, 3) ne doit plus être dans la liste des libres

    def test_est_position_libre(self):
        """Test pour vérifier si une position est libre."""
        self.assertTrue(self.espace_marche.est_position_libre(4, 4))  # La position (4, 4) est libre
        self.espace_marche.ajouter_marchand(self.marchand_1, 4, 4)
        self.assertFalse(self.espace_marche.est_position_libre(4, 4))  # La position (4, 4) est maintenant occupée

if __name__ == '__main__':
    unittest.main()
