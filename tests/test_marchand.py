import unittest
from dependency_injector.wiring import inject, Provide
from core.classes.Marchand import Marchand
from core.dependency_injection.container import Container
from core.enums.TypeMarchandEnum import TypeMarchandEnum

class TestMarchand(unittest.TestCase):

    def setUp(self):
        """Initialisation d'un marché et d'un marchand pour les tests."""
        self.container = Container()  # Créez une instance du container
        self.container.init_resources()  # Charge toutes les ressources de l'application
        self.container.wire()  # Applique le wiring pour l'injection

        # Injecter explicitement mongo_handler dans l'objet Marchand
        mongo_handler = self.container.marchand_handler()  # Obtenir le handler
        self.marchand = Marchand(
            nom="Dohi", prenom="Azalakapinhou", telephone="0123456789", adresse="1 rue de Vogan",
            description="Vendeur de fruits", type_marchand=TypeMarchandEnum.GROSSISTE,
            username="XXXX", password="XXXXXXXXXXXXX",
            mongo_handler=mongo_handler  # Passer mongo_handler comme argument
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

    def test_save(self):
        """Vérifie que la méthode save fonctionne correctement."""
        self.container = Container()  # Créez une instance du container
        self.container.init_resources()  # Charge toutes les ressources de l'application
        self.container.wire()
        self.marchand.save()
        # Vous pouvez ici ajouter des assertions pour vérifier si la sauvegarde a bien eu lieu.
        # Par exemple, vérifier que l'ID du marchand a été défini après l'appel de save.
        self.assertIsNotNone(self.marchand.id)


if __name__ == '__main__':
    unittest.main()