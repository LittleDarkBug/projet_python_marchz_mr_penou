
# Projet Mr plenou
## Structure du projet

```text
📦
├─ .github
│  └─ workflows
│     ├─ pylint.yml
│     └─ python-app.yml
├─ .gitignore
├─ .vscode
│  └─ settings.json
├─ LICENSE
├─ README.md
├─ core
│  ├─ classes
│  │  ├─ Admin.py
│  │  ├─ CategorieProduit.py
│  │  ├─ Client.py
│  │  ├─ CodePromo.py
│  │  ├─ CouponGenerique.py
│  │  ├─ EspaceMarche.py
│  │  ├─ FactureVente.py
│  │  ├─ Fournisseur.py
│  │  ├─ LigneVente.py
│  │  ├─ Marchand.py
│  │  ├─ Notification.py
│  │  ├─ NotificationSingletonService.py
│  │  ├─ Produit.py
│  │  ├─ Utilisateur.py
│  │  └─ __pycache__
│  ├─ data
│  │  ├─ __pycache__
│  │  │  └─ connection.cpython-313.pyc
│  │  └─ connection.py
│  ├─ enums
│  │  ├─ ModaliteVenteEnum.py
│  │  ├─ TypeMarchandEnum.py
│  │  └─ TypeUniteEnum.py
│  ├─ services
│  │  └─ AuthService.py
│  └─ utils
│     ├─ PasswordUtils.py
│     └─ Recommandation.py
├─ databases
│  └─ docker-compose.yaml
├─ demos
│  ├─ achat_client.py
│  ├─ espace_marche.py
│  ├─ historiques.py
│  ├─ marchands_produits.py
│  └─ optimisation_recherche.py
├─ main.py
├─ main_utils.py
├─ requirements.txt
└─ tests
   ├─ __init__.py
   ├─ __pycache__
   │  ├─ test_connection_layer.cpython-313.pyc
   │  ├─ test_espace_marche.cpython-313.pyc
   │  └─ test_marchand.cpython-313.pyc
   ├─ test_connection_layer.py
   ├─ test_espace_marche.py
   └─ test_marchand.py
```

## Description des Composants

### **`core/`**  
Ce répertoire contient la logique centrale du projet et est organisé en sous-dossiers afin de favoriser la modularité et la maintenabilité.

- **`classes/`** : Contient les fichiers des principales classes du projet. Chaque classe est responsable d'un aspect spécifique de l'application, allant des utilisateurs (`Utilisateur.py`) à la gestion des produits (`Produit.py`) et des ventes (`FactureVente.py`, `LigneVente.py`).
- **`data/`** : Contient la gestion des connexions à la base de données, avec le fichier `connection.py` gérant les interactions avec la base de données.
- **`enums/`** : Contient les énumérations utilisées dans l'application pour définir les types, les modes de vente (`ModaliteVenteEnum.py`), et d'autres catégories.
- **`services/`** : Fournit des services comme l'authentification (`AuthService.py`), permettant de centraliser la gestion de la logique métier.
- **`utils/`** : Contient des utilitaires généraux pour le projet, comme la gestion des mots de passe (`PasswordUtils.py`) ou des recommandations (`Recommandation.py`).

### **`databases/`**  
Ce dossier contient des fichiers de configuration pour la gestion des bases de données, notamment un fichier `docker-compose.yaml` pour configurer la base de données dans un environnement Docker.

### **`demos/`**  
Des scripts de démonstration sont inclus ici, montrant des cas d'utilisation de l'application, comme des achats clients (`achat_client.py`), des exemples d'optimisation de recherche (`optimisation_recherche.py`), et la gestion des marchands et des produits (`marchands_produits.py`).

### **`main.py`**  
Point d'entrée du programme. Ce fichier montre comment initialiser et utiliser les classes et services définis dans `core/`.

### **`main_utils.py`**  
Contient des fonctions utilitaires supplémentaires utilisées dans `main.py` et ailleurs dans le projet.

### **`tests/`**  
Ce répertoire contient les tests unitaires pour le projet. Chaque fichier de test vérifie une partie spécifique de l'application. Par exemple, `test_connection_layer.py` teste la couche de connexion à la base de données, et `test_marchand.py` vérifie la gestion des marchands.

### **`requirements.txt`**  
Liste les dépendances Python nécessaires pour exécuter le projet. Pour installer ces dépendances, vous pouvez utiliser la commande :
```bash
pip install -r requirements.txt
```

### **`LICENSE`**  
Contient les informations relatives à la licence du projet.

### **`.gitignore`**  
Spécifie les fichiers et répertoires à exclure du contrôle de version Git.

## Prérequis

- **Docker** est nécessaire pour la gestion des bases de données et des services externes dans le projet. Vous devez avoir Docker installé sur votre machine pour utiliser correctement les configurations de base de données définies dans `docker-compose.yaml` sous le répertoire `databases/`.

- **Python** : Ce projet est développé en Python, et il est recommandé de travailler dans un environnement virtuel isolé pour gérer les dépendances spécifiques au projet.

## Installation

### 1. Créer un environnement virtuel (venv)

Pour garantir une installation propre et éviter des conflits de dépendances, il est recommandé de créer un environnement virtuel Python. Voici comment faire :

```bash
# Créer un environnement virtuel (si vous n'en avez pas déjà un)
python3 -m venv venv

# Activer l'environnement virtuel
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate
```

### 2. Installer les dépendances

Ensuite, installez les dépendances du projet :

```bash
pip install -r requirements.txt
```

### 3. Configurer Docker

Le projet utilise Docker pour gérer la base de données. Vous pouvez utiliser `docker-compose` pour démarrer les services nécessaires :

```bash
docker-compose up
```

Cela lancera les conteneurs définis dans le fichier `docker-compose.yaml` situé dans le répertoire `databases/`.

## Démarrage

1. Après avoir configuré Docker et installé les dépendances, vous pouvez démarrer l'application avec le fichier `main.py`. Ce fichier sert de point d'entrée et montre comment utiliser les services définis dans le projet.

   ```bash
   python main.py
   ```

2. Pour lancer les tests unitaires et vérifier que tout fonctionne comme prévu, utilisez :

   ```bash
   python -m unittest discover -s tests
   ```

---