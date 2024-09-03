from src.core._shared.domain.notification import Notification
from src.core.cast_member.domain.cast_member_type import CastMemberType


class CastMemberValidator:

    @staticmethod
    def create(name: str, cast_member_type: CastMemberType):
        notification = Notification()

        if len(name) > 255:
            notification.add_error("name cannot be longer than 255")

        if not name:
            notification.add_error("name cannot be empty")

        if cast_member_type not in CastMemberType:
            notification.add_error(
                "type must be a valid CastMemberType: actor or director"
            )
        
        return notification
