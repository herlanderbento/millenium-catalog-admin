import pytest

from src.core.cast_member.domain.cast_member_type import CastMemberType
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMemberInput,
    CreateCastMemberOutput,
    CreateCastMemberUseCase,
)
from src.django_project.cast_member_app.repository import CastMemberDjangoRepository


@pytest.mark.django_db
class TestCreateCastMemberUseCaseInt:
    use_case: CreateCastMemberUseCase
    cast_member_repo: CastMemberDjangoRepository

    def setup_method(self) -> None:
        self.cast_member_repo = CastMemberDjangoRepository()
        self.use_case = CreateCastMemberUseCase(self.cast_member_repo)

    def test_create_cast_member(self):
        input = CreateCastMemberInput(
            name="director example",
            type=CastMemberType.DIRECTOR,
        )
        output = self.use_case.execute(input)

        cast_member_created = self.cast_member_repo.find_by_id(output.id)

        assert output == CreateCastMemberOutput(
            id=cast_member_created.id.value,
            name="director example",
            type=CastMemberType.DIRECTOR,
            created_at=cast_member_created.created_at,
        )

        input = CreateCastMemberInput(
            name="actor example",
            type=CastMemberType.ACTOR,
        )
        output = self.use_case.execute(input)

        cast_member_created = self.cast_member_repo.find_by_id(output.id)

        assert output == CreateCastMemberOutput(
            id=cast_member_created.id.value,
            name="actor example",
            type=CastMemberType.ACTOR,
            created_at=cast_member_created.created_at,
        )
