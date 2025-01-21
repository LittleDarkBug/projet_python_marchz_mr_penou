class Fournisseur:
    def __init__(self, nom, adresse, telephone, email):
        self._nom = nom
        self._adresse = adresse
        self._telephone = telephone
        self._email = email
    
    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, value):
        self._nom = value

    @property
    def adresse(self):
        return self._adresse
    
    @adresse.setter
    def adresse(self, value):
        self._adresse = value

    @property
    def telephone(self):
        return self._telephone
    
    @telephone.setter
    def telephone(self, value):
        self._telephone = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value