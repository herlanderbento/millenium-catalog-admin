from src.core.cast_member.domain.cast_member_type import CastMemberType


class CastMemberValidator:
    @staticmethod
    def create(name: str, cast_member_type: CastMemberType):
        if len(name) > 255:
            raise ValueError("name cannot be longer than 255")

        if not name:
            raise ValueError("name cannot be empty")

        if cast_member_type not in CastMemberType:
            raise ValueError("type must be a valid CastMemberType: actor or director")
