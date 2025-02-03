from mongoengine import Document, StringField, ListField, IntField, ReferenceField
from typing import List, Tuple
from core.classes.Marchand import Marchand
import plotly.graph_objects as go


class EspaceMarche(Document):
    """
    Représente un espace de marché dans MongoDB.
    """
    nom = StringField(required=True)
    taille = ListField(IntField(), required=True)  # Taille est une liste de deux entiers [x_max, y_max]
    marchands = ListField(ReferenceField(Marchand))  # Liste de références à des objets 'Marchand'
    
    # Méthodes pour manipuler les marchands et leurs positions
    def est_position_libre(self, x: int, y: int) -> bool:
        """
        Vérifie si la position (x, y) est libre dans l'espace de marché.

        Args:
            x (int): La coordonnée x de la position.
            y (int): La coordonnée y de la position.

        Returns:
            bool: True si la position est libre, False sinon.
        """
        for marchand_ref in self.marchands:
            # Charger le marchand complet depuis la référence
            marchand = Marchand.objects(id=marchand_ref.id).first()
            if marchand and marchand.x == x and marchand.y == y:
                return False
        return True

    def ajouter_marchand(self, marchand: Marchand, x: int, y: int) -> None:
        """
        Ajoute un marchand à une position libre dans l'espace de marché en lui assignant une position (x, y).

        Args:
            marchand (Marchand): Le marchand à ajouter.
            x (int): La coordonnée x de la position.
            y (int): La coordonnée y de la position.

        Raises:
            ValueError: Si la position est déjà occupée.
        """
        if self.est_position_libre(x, y):
            print("im here")
            marchand.x = x  # Assigner la position x au marchand
            marchand.y = y  # Assigner la position y au marchand
            self.marchands.append(marchand)  # Ajouter le marchand au marché
            marchand.save()  # Sauvegarder le marchand dans la base de données
            self.save()
        else:
            raise ValueError(f"La position ({x}, {y}) est déjà occupée.")
    
    def retirer_marchand(self, marchand: Marchand) -> None:
        """
        Retire un marchand de l'espace de marché.
        """
        self.marchands.remove(marchand)
        marchand.save()
        self.save()

    def obtenir_emplacements_libres(self) -> List[Tuple[int, int]]:
        """
        Retourne une liste d'emplacements libres dans l'espace de marché.

        Returns:
            List[Tuple[int, int]]: Liste des coordonnées (x, y) des emplacements libres.
        """
        emplacements_libres = []
        for x in range(self.taille[0]):  # Parcourt les x possibles
            for y in range(self.taille[1]):  # Parcourt les y possibles
                if self.est_position_libre(x, y):
                    emplacements_libres.append((x, y))  # Ajoute la position libre
        return emplacements_libres

    def generer_graphique(self):
        """Génère un graphique interactif affichant les marchands avec des couleurs selon leur niveau de stock."""
        fig = go.Figure()

        # Définition des seuils de stock
        seuil_bas = 10   # En dessous de 10 : stock faible
        seuil_haut = 50  # Au-dessus de 50 : stock élevé

        # Définition des couleurs en fonction du stock
        def determiner_couleur(stock):
            if stock > seuil_haut:
                return "green"  # Stock élevé
            elif stock >= seuil_bas:
                return "orange"  # Stock moyen
            else:
                return "red"  # Stock faible

        for marchand_ref in self.marchands:
                    # Charger le marchand complet depuis la référence
            marchand = Marchand.objects(id=marchand_ref.id).first()
            print(marchand)
            if not marchand:
                continue
            stock = marchand.niveau_de_stock  # Retourne un entier
            couleur = determiner_couleur(stock)

            info_marchand = (
                f"Nom: {marchand.nom} {marchand.prenom}<br>"
                f"Type: {marchand.type_marchand}<br>"
                f"Téléphone: {marchand.telephone}<br>"
                f"Description: {marchand.description}<br>"
                f"Niveau de stock: {stock}"
            )

            fig.add_trace(go.Scatter(
                x=[marchand.x], 
                y=[marchand.y],
                mode='markers+text',
                marker=dict(size=12, color=couleur),
                text=[info_marchand],
                textposition="top center",
                name=marchand.username
            ))

        # Ajout d'une légende explicative
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=12, color="green"), name="Stock élevé (> 50)"))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=12, color="orange"), name="Stock moyen (10 - 50)"))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=12, color="red"), name="Stock faible (< 10)"))

        fig.update_layout(
            title=f"Répartition des marchands dans {self.nom}",
            xaxis_title="X",
            yaxis_title="Y",
            xaxis=dict(range=[0, self.taille[0]]),
            yaxis=dict(range=[0, self.taille[1]]),
            width=1280,
            height=720
        )

        return fig

    def __str__(self):
        """Affiche le graphique quand on imprime l'objet."""
        self.generer_graphique().show()
        return f"<EspaceMarche: {self.nom}, {len(self.marchands)} marchands>"


    @classmethod
    def find(cls, criteria: dict):
        """
        Recherche des espaces de marché en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.

        Returns:
            List[dict]: Une liste d'objets d'espace de marché correspondants.
        """
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """
        Recherche un seul espace de marché en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.

        Returns:
            dict: L'espace de marché trouvé, ou None si aucun espace de marché n'est trouvé.
        """
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """
        Recherche un espace de marché par son ID MongoDB.

        Args:
            id (str): L'ID MongoDB de l'espace de marché à rechercher.

        Returns:
            dict: L'espace de marché trouvé, ou None si aucun espace de marché n'est trouvé.
        """
        return cls.objects(id=id).first()
