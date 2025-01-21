class Notification:
    def __init__(self, type_notification: str, message: str) -> None:
        self._type_notification = type_notification
        self._message = message

    @property
    def type_notification(self) -> str:
        return self._type_notification

    @type_notification.setter
    def type_notification(self, value: str) -> None:
        self._type_notification = value

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        self._message = value
