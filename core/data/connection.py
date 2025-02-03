import mongoengine as me

def initialize_connection(host='localhost', port=27017, database_name='mrplenou', username='admin', password='admin'):
    """
    Initialise la connexion à MongoDB en utilisant MongoEngine.
    
    Args:
        host (str): L'hôte de la base de données MongoDB (par défaut : 'localhost').
        port (int): Le port de la base de données MongoDB (par défaut : 27017).
        database_name (str): Le nom de la base de données à utiliser (par défaut : 'mrplenou').
        username (str): Le nom d'utilisateur MongoDB.
        password (str): Le mot de passe MongoDB.

    Raises:
        mongoengine.connection.MongoEngineConnectionError: Si la connexion échoue.
    """
    try:
        me.connect(
            db=database_name,
            username=username,
            password=password,
            host=host,
            port=port
        )
        print(f"Connexion à MongoDB sur {host}:{port}, base de données: {database_name}")
    except me.connection.MongoEngineConnectionError as e:
        raise Exception(f"Échec de la connexion à MongoDB : {e}")

def close_connection():
    """
    Ferme la connexion MongoDB active via MongoEngine.
    """
    me.disconnect()
    print("Connexion MongoDB fermée.")
