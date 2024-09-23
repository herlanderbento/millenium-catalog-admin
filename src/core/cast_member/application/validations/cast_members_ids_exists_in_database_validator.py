from typing import List, Union
from uuid import UUID
from src.core._shared.domain.exceptions import NotFoundException
from src.core.cast_member.domain.cast_member import CastMember, CastMemberId
from src.core.cast_member.domain.cast_member_repository import ICastMemberRepository


class CastMembersIdExistsInDatabaseValidator:
    def __init__(self, cast_member_repo: ICastMemberRepository):
        self.cast_member_repo = cast_member_repo

    def validate(
        self, cast_members_id: set[CastMemberId]
    ) -> Union[List[UUID], List[NotFoundException]]:
        exists_result = self.cast_member_repo.exists_by_id(cast_members_id)

        if exists_result["not_exists"]:
            not_found_ids = [str(id) for id in exists_result["not_exists"]]
            raise NotFoundException(", ".join(not_found_ids), CastMember)

        return cast_members_id
