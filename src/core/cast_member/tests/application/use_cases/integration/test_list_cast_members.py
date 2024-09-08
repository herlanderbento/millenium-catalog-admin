import datetime
from uuid import UUID

import pytest
from core.cast_member.domain.cast_member_repository import CastMemberFilter
from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
)
from src.core.cast_member.application.use_cases.list_cast_members import (
    ListCastMembersInput,
    ListCastMembersOutput,
    ListCastMembersUseCase,
)
from src.django_project.cast_member_app.repository import CastMemberDjangoRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


@pytest.mark.django_db
class TestListCastMembersUseCase:
    use_case: ListCastMembersUseCase
    cast_member_repo: CastMemberDjangoRepository

    def setup_method(self) -> None:
        self.cast_member_repo = CastMemberDjangoRepository()
        self.use_case = ListCastMembersUseCase(self.cast_member_repo)

    def test_should_be_able_list_cast_members(self):
        items = [
            CastMember(name="test 1", type=CastMemberType.DIRECTOR),
            CastMember(
                name="test 2",
                type=CastMemberType.DIRECTOR,
                created_at=datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(seconds=200),
            ),
        ]
        self.cast_member_repo.bulk_insert(items)
        input = ListCastMembersInput()
        output = self.use_case.execute(input)
        assert output == ListCastMembersOutput(
            items=list(map(CastMemberOutput.from_entity, items[::-1])),
            total=2,
            current_page=1,
            per_page=15,
            last_page=1,
        )
