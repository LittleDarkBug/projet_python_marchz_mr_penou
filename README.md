## Description des Composants

- **`core/`** : Contient toutes les fonctionnalités principales du package. Chaque classe est placée dans un fichier distinct afin d'assurer modularité et maintenabilité.  
- **`services.py`** : Implémente un système léger d'injection de dépendances permettant de gérer et d'accéder à différents services (par exemple, des classes ou des utilitaires).  
- **`main.py`** : Point d'entrée du package. Montre comment initialiser et utiliser les services fournis par le package.  
- **`tests/`** : Contient les tests unitaires pour le package. Chaque fichier de test correspond à un module ou une classe spécifique dans le répertoire `core/`.  
- **`requirements.txt`** : Liste des dépendances Python nécessaires pour le package.  
- **`LICENSE`** : Informations relatives à la licence du package.  
- **`.gitignore`** : Spécifie les fichiers et répertoires à exclure du contrôle de version.  

## Utilisation

1. Clonez ou copiez cette structure de package dans votre répertoire souhaité.  
2. Implémentez vos classes dans le répertoire `core/`, en veillant à placer chaque classe dans un fichier séparé.  
3. Utilisez `services.py` pour gérer et accéder à vos classes via le système d'injection de dépendances.  
4. Rédigez les tests pour vos classes dans le répertoire `tests/`.  
5. Utilisez `main.py` comme exemple ou point de départ pour exécuter le package.  

## Démarrage

1. Installez les dépendances :  
   ```bash
   pip install -r requirements.txt
   ```
2. Lancez les tests : 
    ```bash
    python -m unittest discover -s tests
   ```