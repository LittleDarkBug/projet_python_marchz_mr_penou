import unittest
from core.data.connection import MongoDBConnection

class TestConnectionLayer(unittest.TestCase):

    def setUp(self):
        """Initialiser une instance de notre  MongoDBConnection:
        Une classe singleton pour gérer la connexion à MongoDB.
        """
        self.mongo_db_connection = MongoDBConnection()

    def test_singleton_instance(self):
        """Vérifier que deux instances de MongoDBConnection sont identiques."""
        another_mongo_db_connection = MongoDBConnection()
        self.assertIs(self.mongo_db_connection, another_mongo_db_connection)
        self.assertIs(self.mongo_db_connection.client, another_mongo_db_connection.client)
        self.assertIs(self.mongo_db_connection.db, another_mongo_db_connection.db)
        self.mongo_db_connection.client.close()
    
    def test_initialise_connection( self ):
        """Vérifier que la connexion à MongoDB est établie."""
        self.mongo_db_connection._initialize_connection()
        self.assertIsNotNone(self.mongo_db_connection.client)
        self.assertIsNotNone(self.mongo_db_connection.db)
        self.mongo_db_connection.client.close()

    def test_get_db(self ):
        """Vérifier que la méthode get_db renvoie une instance de la base de données."""
        self.mongo_db_connection._initialize_connection()
        db = self.mongo_db_connection.get_db()
        self.assertIsNotNone(db)
        self.assertEqual(db, self.mongo_db_connection.db)
        self.mongo_db_connection.client.close()

    def test_close_connection(self ):
        """Vérifier que la méthode close_connection ferme la connexion à MongoDB."""
        self.mongo_db_connection.close_connection()
        self.assertIsNone(self.mongo_db_connection.client)


if __name__ == '__main__':
    unittest.main()
