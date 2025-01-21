class CategorieProduit:
    def __init__(self, libelle: str, description: str) -> None:
        self._libelle = libelle
        self._description = description

    @property
    def libelle(self) -> str:
        return self._libelle

    @libelle.setter
    def libelle(self, value: str) -> None:
        self._libelle = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value