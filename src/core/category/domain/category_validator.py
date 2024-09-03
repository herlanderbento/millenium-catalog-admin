from src.core._shared.domain.notification import Notification


class CategoryValidator:

    @staticmethod
    def create(name: str, description: str) -> Notification:
        notification = Notification()

        if len(name) > 255:
            notification.add_error("name cannot be longer than 255")

        if not name:
            notification.add_error("name cannot be empty")

        if len(description) > 1024:
            notification.add_error("description cannot be longer than 1024")

        return notification
