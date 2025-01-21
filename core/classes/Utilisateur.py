class Utilisateur:
    def __init__(self, nom: str, prenom: str, telephone: str, adresse: str, description: str) -> None:
        self._nom = nom
        self._prenom = prenom
        self._telephone = telephone
        self._adresse = adresse
        self._description = description

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, value: str) -> None:
        self._nom = value

    @property
    def prenom(self) -> str:
        return self._prenom

    @prenom.setter
    def prenom(self, value: str) -> None:
        self._prenom = value

    @property
    def telephone(self) -> str:
        return self._telephone

    @telephone.setter
    def telephone(self, value: str) -> None:
        self._telephone = value

    @property
    def adresse(self) -> str:
        return self._adresse

    @adresse.setter
    def adresse(self, value: str) -> None:
        self._adresse = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value