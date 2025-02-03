from mongoengine import Document, StringField

class Notification(Document):
    type_notification = StringField(required=True)
    message = StringField(required=True)

    def __str__(self):
        return f"[{self.type_notification}] {self.message}"

    @classmethod
    def find(cls, criteria: dict):
        """Recherche des notifications en fonction des critères."""
        return cls.objects(__raw__=criteria)

    @classmethod
    def find_one(cls, criteria: dict):
        """Recherche une seule notification en fonction des critères."""
        return cls.objects(__raw__=criteria).first()

    @classmethod
    def find_by_id(cls, id: str):
        """Recherche une notification par son ID."""
        return cls.objects(id=id).first()
