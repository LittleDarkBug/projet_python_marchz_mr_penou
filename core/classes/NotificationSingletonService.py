from Notification import Notification

class NotificationSingletonService:
    _instance = None

    def __new__(cls) -> "NotificationSingletonService":
        if cls._instance is None:
            cls._instance = super(NotificationSingletonService, cls).__new__(cls)
        return cls._instance

    def send_notification(self, notification: Notification) -> None:
        # Logic to send notification
        print(f"Notification sent: {notification.type_notification} - {notification.message}")
