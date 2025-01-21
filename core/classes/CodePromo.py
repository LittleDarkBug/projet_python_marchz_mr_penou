from CouponGenerique import CouponGenerique
from datetime import DateTime

class CodePromo(CouponGenerique):
    def __init__(self, actif: bool, cumulable: bool, date_expiration: DateTime, reduction_montant: float, reduction_taux: float, global_coupon: bool, max_usage_per_user: int, all_users: bool, code: str) -> None:
        super().__init__(actif, cumulable, date_expiration, reduction_montant, reduction_taux, global_coupon)
        self._max_usage_per_user = max_usage_per_user
        self._all_users = all_users
        self._code = code

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
