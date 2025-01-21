import unittest
from core.classes.Marchand import Marchand
from core.enums.TypeMarchandEnum import TypeMarchandEnum

class TestMarchand(unittest.TestCase):

    def setUp(self):
        """Initialisation d'un marché et d'un marchand pour les tests."""
        self.marchand = Marchand(
            nom="Dohi", prenom="Azalakapinhou", telephone="0123456789", adresse="1 rue de Vogan", 
            description="Vendeur de fruits", type_marchand=TypeMarchandEnum.GROSSISTE
        )

    def test_initialisation_marchand(self):
        """Vérifie que le marchand est initialisé correctement."""
        self.assertEqual(self.marchand.nom, "Dohi")
        self.assertEqual(self.marchand.prenom, "Azalakapinhou")
        self.assertEqual(self.marchand.telephone, "0123456789")
        self.assertEqual(self.marchand.adresse, "1 rue de Vogan")
        self.assertEqual(self.marchand.description, "Vendeur de fruits")
        self.assertEqual(self.marchand.type_marchand, TypeMarchandEnum.GROSSISTE)
        self.assertIsNone(self.marchand.x)
        self.assertIsNone(self.marchand.y)

if __name__ == '__main__':
    unittest.main()
