import uuid
import pytest

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_type import CastMemberType
from src.core._shared.domain.exceptions import NotFoundException
from src.django_project.cast_member_app.repository import CastMemberDjangoRepository
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMemberInput,
    UpdateCastMemberOutput,
    UpdateCastMemberUseCase,
)


@pytest.mark.django_db
class TestUpdateCastMemberUseCaseInt:

    use_case: UpdateCastMemberUseCase
    cast_member_repo: CastMemberDjangoRepository

    def setup_method(self) -> None:
        self.cast_member_repo = CastMemberDjangoRepository()
        self.use_case = UpdateCastMemberUseCase(self.cast_member_repo)

    def test_throw_exception_when_cast_member_not_found(self):
        _id = uuid.uuid4()
        request = UpdateCastMemberInput(id=_id, name="John", type=CastMemberType.ACTOR)
        with pytest.raises(NotFoundException) as assert_error:
            self.use_case.execute(request)
        assert assert_error.value.args[0] == f"CastMember with id {str(_id)} not found"

    def test_must_be_able_to_update_a_cast_member(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.DIRECTOR)
        self.cast_member_repo.insert(cast_member)

        input = UpdateCastMemberInput(
            id=cast_member.id.value,
            name="Herlander Bento",
            type=CastMemberType.ACTOR,
        )

        output = self.use_case.execute(input)

        assert output == UpdateCastMemberOutput(
            id=cast_member.id.value,
            name="Herlander Bento",
            type=CastMemberType.ACTOR,
            created_at=cast_member.created_at,
        )
