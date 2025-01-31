from bson import ObjectId
from CouponGenerique import CouponGenerique
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from core.data.mongo_handler import MongoDBHandler
from core.dependency_injection.container import Container

class CodePromo(CouponGenerique):
    @inject
    def __init__(self, 
                 actif: bool, 
                 cumulable: bool, 
                 date_expiration: datetime, 
                 reduction_montant: float, 
                 reduction_taux: float, 
                 global_coupon: bool, 
                 max_usage_per_user: int, 
                 all_users: bool, 
                 code: str, 
                 mongo_handler: MongoDBHandler = Provide[Container.code_promo_handler]) -> None:
        """
        Initialise un code promo avec les détails associés et l'injection du handler MongoDB.

        Args:
            actif (bool): Indique si le code promo est actif.
            cumulable (bool): Indique si le code promo est cumulable avec d'autres.
            date_expiration (datetime): Date d'expiration du code promo.
            reduction_montant (float): Montant de réduction fixe.
            reduction_taux (float): Taux de réduction en pourcentage.
            global_coupon (bool): Si le coupon est global.
            max_usage_per_user (int): Nombre maximum d'utilisations par utilisateur.
            all_users (bool): Si le code promo s'applique à tous les utilisateurs.
            code (str): Le code promo unique.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.
        """
        super().__init__(actif, cumulable, date_expiration, reduction_montant, reduction_taux, global_coupon)
        self._max_usage_per_user = max_usage_per_user
        self._all_users = all_users
        self._code = code
        self.mongo_handler = mongo_handler

    @property
    def max_usage_per_user(self) -> int:
        return self._max_usage_per_user

    @max_usage_per_user.setter
    def max_usage_per_user(self, value: int) -> None:
        self._max_usage_per_user = value

    @property
    def all_users(self) -> bool:
        return self._all_users

    @all_users.setter
    def all_users(self, value: bool) -> None:
        self._all_users = value

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, value: str) -> None:
        self._code = value

    def is_valid(self) -> bool:
        """
        Vérifie si le code promo est toujours valide en fonction de la date d'expiration et de son statut actif.

        Returns:
            bool: True si le code est valide, sinon False.
        """
        return self.actif and (self.date_expiration > datetime.now())

    def apply_discount(self, montant: float) -> float:
        """
        Applique la réduction sur un montant donné.

        Args:
            montant (float): Montant sur lequel la réduction sera appliquée.

        Returns:
            float: Le montant après application de la réduction.
        """
        if self.reduction_montant:
            return montant - self.reduction_montant
        elif self.reduction_taux:
            return montant * (1 - self.reduction_taux / 100)
        return montant

    def usage_limit_reached(self, usage_count: int) -> bool:
        """
        Vérifie si le nombre d'utilisations par utilisateur a été atteint.

        Args:
            usage_count (int): Le nombre d'utilisations déjà effectuées par l'utilisateur.

        Returns:
            bool: True si la limite est atteinte, sinon False.
        """
        return usage_count >= self.max_usage_per_user

    def is_applicable_to_user(self, user_id: str) -> bool:
        """
        Vérifie si le code promo s'applique à un utilisateur donné.

        Args:
            user_id (str): Identifiant de l'utilisateur.

        Returns:
            bool: True si le code s'applique à l'utilisateur, sinon False.
        """
        if self.all_users:
            return True
        # Ajoute ici toute logique de vérification spécifique aux utilisateurs, par exemple en fonction de leur ID.
        return False

    @inject
    def save(self) -> None:
        """
        Sauvegarde le code promo dans la base de données MongoDB.
        """
        data = {
            'code': self._code,
            'actif': self.actif,
            'cumulable': self.cumulable,
            'date_expiration': self.date_expiration,
            'reduction_montant': self.reduction_montant,
            'reduction_taux': self.reduction_taux,
            'global_coupon': self.global_coupon,
            'max_usage_per_user': self._max_usage_per_user,
            'all_users': self._all_users
        }
        result = self.mongo_handler.save(data)
        self._id = str(result.inserted_id)  # Stocke l'ID du coupon créé
        
    @inject
    def delete(self) -> None:
        """
        Supprime le code promo de la base de données MongoDB.
        """
        if self._id:
            self.mongo_handler.delete({'_id': ObjectId(self._id)})
            self._id = None  # Réinitialise l'ID après suppression
        else:
            raise ValueError("Impossible de supprimer un code promo sans ID.")

    @classmethod
    @inject
    def find(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.code_promo_handler]):
        """
        Recherche des codes promo en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            Cursor: Un curseur MongoDB pour parcourir les documents trouvés.
        """
        return mongo_handler.find(criteria)

    @classmethod
    @inject
    def find_one(cls, criteria: dict, mongo_handler: MongoDBHandler = Provide[Container.code_promo_handler]):
        """
        Recherche un seul code promo en fonction des critères spécifiés.

        Args:
            criteria (dict): Un dictionnaire de critères de recherche.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données du code promo trouvé, ou None si aucun code promo n'est trouvé.
        """
        return mongo_handler.find_one(criteria)

    @classmethod
    @inject
    def find_by_id(cls, id: str, mongo_handler: MongoDBHandler = Provide[Container.code_promo_handler]):
        """
        Recherche un code promo par son ID MongoDB.

        Args:
            id (str): L'ID MongoDB du code promo à rechercher.
            mongo_handler (MongoDBHandler): Le handler MongoDB injecté automatiquement.

        Returns:
            dict: Les données du code promo trouvé, ou None si aucun code promo n'est trouvé.
        """
        return mongo_handler.find_by_id(ObjectId(id))
