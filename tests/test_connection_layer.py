import unittest
from core.data.connection import initialize_connection, close_connection
import mongoengine as me

class TestConnectionLayer(unittest.TestCase):

    def setUp(self):
        """Initialiser une connexion à MongoDB pour les tests."""
        initialize_connection(database_name='mrplenou_tests')
        
    def tearDown(self):
        """Fermer la connexion après chaque test."""
        close_connection()

    def test_initialize_connection(self):
        """Vérifier que la connexion à MongoDB est bien établie."""
        # Vérifie que la connexion est active
        self.assertNotEqual(me.connection._get_db(), None)

    def test_close_connection(self):
        """Vérifier que la connexion à MongoDB est correctement fermée."""
        close_connection()
        # Vérifie que la connexion est fermée
        self.assertNotIn('connection', me.connection._connections)

if __name__ == '__main__':
    unittest.main()
