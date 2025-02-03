from core.classes.Utilisateur import Utilisateur
from core.classes.FactureVente import FactureVente
from typing import List
from mongoengine import Document, StringField, BooleanField, ListField, ReferenceField
from core.utils.PasswordUtils import PasswordUtils

class Client(Utilisateur):
    """
    Classe représentant un client dans MongoDB avec des fonctionnalités étendues.
    """
    liste_achats = ListField(ReferenceField(FactureVente))

    meta = {
        'collection': 'clients'  # Nom de la collection
    }


    def add_achat(self, facture: FactureVente) -> None:
        """Ajoute une facture à la liste des achats du client."""
        self.liste_achats.append(facture)

    def remove_achat(self, facture: FactureVente) -> None:
        """Retire une facture de la liste des achats du client."""
        if facture in self.liste_achats:
            self.liste_achats.remove(facture)
        else:
            raise ValueError("Cette facture n'est pas présente dans la liste des achats.")

    def save(self) -> None:
        """Sauvegarde le client dans MongoDB."""
        super().save()

    def delete(self) -> None:
        """Supprime le client de MongoDB."""
        if self.id:
            self.delete()
        else:
            raise ValueError("Impossible de supprimer un client sans ID.")

    @classmethod
    def find(cls, criteria: dict):
        """Recherche des clients en fonction des critères spécifiés."""
        return cls.objects(**criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """Recherche un seul client en fonction des critères spécifiés."""
        return cls.objects(**criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """Recherche un client par son ID MongoDB."""
        return cls.objects(id=id).first()
